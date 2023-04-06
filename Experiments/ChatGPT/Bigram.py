import torch
import torch.nn as nn
from torch.nn import functional as F
from ChatGPT.Config import Config

'''
    1) Start off simple bi-gram model
    2) change to token embedding
    3) Add positional encoding
    4) Add attention
    5) Add computation (ffwd)
    6) Build a Block = attention + computation
    7) Add residual x = x + sa_head (Optimization since our network is pretty deep now
    8) LayerNorm (based on BatchNorm)
    9) Add Dropout
    9) Scale up

'''
class BigramLanguageModel(nn.Module):
    def __init__(self, cfg: Config):
        super().__init__()
        self.to(cfg.device)
        torch.manual_seed(1337)
        self.device = cfg.device
        self.block_size = cfg.block_size
        n_layer = cfg.num_layers

        self.token_embedding_table = nn.Embedding(cfg.vocab_size, cfg.embedding_dims)
        self.position_embedding_table = nn.Embedding(cfg.block_size, cfg.embedding_dims)
        self.blocks = nn.Sequential(*[Block(cfg) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(cfg.embedding_dims)
        self.lm_head = nn.Linear(cfg.embedding_dims, cfg.vocab_size)

    def forward(self, idx, targets=None):
        # idx and targets are both (B, T)
        B, T = idx.shape

        # Batch x Time x channel
        tok_embedding = self.token_embedding_table(idx)  # (B, T, C)
        pos_embedding = self.position_embedding_table(torch.arange(T, device=self.device))
        x = tok_embedding + pos_embedding
        x = self.blocks(x)
        x = self.ln_f(x)
        logits = self.lm_head(x)

        if targets is None:
            loss = None
        else:
            B, T, C = logits.shape
            logits = logits.view(B*T, C)
            targets = targets.view(B*T)
            loss = F.cross_entropy(logits, targets)

        return logits, loss

    def generate(self, idx, max_new_tokens):
        # idx is (B, T) array of indices in the current context
        for _ in range(max_new_tokens):
            b, t = idx.shape
            if t < self.block_size:
                idx_cond = idx[:, :]
            else:
                idx_cond = idx[:, -self.block_size:]

            logits, loss = self(idx_cond)

            # look at last time step only
            logits = logits[:, -1, :]   # Becomes (B, C)

            probs = F.softmax(logits, dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)  # (B,1)
            idx = torch.cat((idx, idx_next), dim=1)             # (B, T+1)
        return idx

    def gen_from_scratch(self, num_tokens):
        idx = torch.zeros((1, 1), dtype=torch.long, device=self.device)
        seq = self.generate(idx, max_new_tokens=num_tokens)
        return seq


class Head(nn.Module):
    def __init__(self, cfg: Config):
        super().__init__()
        head_size = cfg.head_size
        n_embed = cfg.embedding_dims
        block_size = cfg.block_size
        self.key = nn.Linear(n_embed, head_size, bias=False)    # This is how you find this node
        self.query = nn.Linear(n_embed, head_size, bias=False)  # This is the query for interesting nodes
                                                                # k.q is a vector of "interesting"
        self.value = nn.Linear(n_embed, head_size, bias=False)  # This is the value for an interesting node
        self.register_buffer("tril", torch.tril(torch.ones(block_size, block_size)))
        self.dropout = nn.Dropout(cfg.dropout)

    def forward(self, x):
        B, T, C = x.shape
        k = self.key(x)      # (B, T, head_size)
        q = self.query(x)

        # compute attention scores, i.e. affinities
        # C normalization keeps softmax from getting to peaky
        weights = q @ k.transpose(-2, -1) * C**-0.5  # (B, T, head_size) @ (B, head_size, T) -> (B, T, T)
        weights = weights.masked_fill(self.tril[:T, :T] == 0, float('-inf'))
        weights = F.softmax(weights, dim=1)
        weights = self.dropout(weights)

        v = self.value(x)
        out = weights @ v
        return out


class MultiHeadAttention(nn.Module):
    def __init__(self, cfg: Config):
        super().__init__()
        cfg = cfg.clone()
        n_emb = cfg.embedding_dims
        num_heads = cfg.num_heads
        cfg.head_size = cfg.head_size // num_heads
        self.heads = nn.ModuleList((Head(cfg) for _ in range(num_heads)))
        self.proj = nn.Linear(n_emb, n_emb)
        self.dropout = nn.Dropout(cfg.dropout)

    def forward(self, x):
        heads = [h(x) for h in self.heads]
        out = torch.cat(heads, dim=-1)
        out = self.proj(out)
        out = self.dropout(out)
        return out


class FeedForward(nn.Module):
    def __init__(self, cfg: Config):
        super().__init__()
        n_emb = cfg.embedding_dims
        self.net = nn.Sequential(
            nn.Linear(n_emb, 4 * n_emb),    # Inner layer has 4x input
            nn.ReLU(),
            nn.Linear(4 * n_emb, n_emb),     # projection for residual
            nn.Dropout(cfg.dropout)
        )

    def forward(self, x):
        return self.net(x)


class Block(nn.Module):
    ''' communication via attention + computation'''
    def __init__(self, cfg):
        super().__init__()
        self.sa = MultiHeadAttention(cfg)
        self.ffwd = FeedForward(cfg)
        self.layer_norm1 = nn.LayerNorm(cfg.embedding_dims)
        self.layer_norm2 = nn.LayerNorm(cfg.embedding_dims)

    def forward(self, x):
        x = self.layer_norm1(x)
        x = x + self.sa(x)      # Add skip connection (residuals)
        x = self.layer_norm2(x)
        x = x + self.ffwd(x)
        return x

class BatchNorm1d:
    def __init__(self, dim, eps=1e-5, momentum=0.1):
        self.eps = eps
        self.gamma = torch.ones(dim)
        self.beta = torch.zeros(dim)

    def __call__(self, x):
        # Calculate the forward pass
        xmean = x.mean(1, keepdim=True)
        xvar = x.var(1, keepdim=True)
        xhat = (x - xmean) / torch.sqrt(xvar + self.eps)    # Normalize to unit vectors
        self.out = self.gamma * xhat + self.beta

    def parameters(self):
        return (self.gamma, self.beta)
