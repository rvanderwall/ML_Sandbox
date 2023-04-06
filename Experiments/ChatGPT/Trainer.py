import torch.optim
import torch.nn as nn
from torch.nn import functional as F
from ChatGPT.Config import Config


class Trainer:
    def __init__(self, cfg: Config, encoder, model, batcher):
        self.encoder = encoder
        self.model = model
        self.batcher = batcher

        self.split = cfg.split
        self.epochs = cfg.epochs
        self.batch_size = cfg.batch_size
        self.eval_iters = cfg.eval_iters
        self.learning_rate = cfg.learning_rate

    def get_train_test_data(self, text):
        data = self.encoder.get_encoded_data(text)
        print(data.shape, data.dtype)
        print(data[:20])

        n = int(self.split * len(data))
        train_set = data[:n]
        val_set = data[n:]
        return train_set, val_set

    def train(self, train_data, test_data):
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=self.learning_rate)

        self.batcher.batch_size = self.batch_size
        for epoch in range(self.epochs):
            # Get batch
            xb, yb = self.batcher.get_batch(train_data)

            # Evaluate
            logits, loss = self.model(xb, yb)
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
            if epoch % 1000 == 0:
                loss = self.estimate_loss(train_data, test_data)
                print(f"{epoch}: train loss {loss['train']:.4f}, val loss {loss['val']:.4f}")

    @torch.no_grad()
    def estimate_loss(self, train_set, test_set):
        out = {}
        self.model.eval()   # Set model to eval
        for lbl, data in [('train', train_set), ('val', test_set)]:
            losses = torch.zeros(self.eval_iters)
            for k in range(self.eval_iters):
                X, Y = self.batcher.get_batch(data)
                logits, loss = self.model(X, Y)
                losses[k] = loss.item()
            out[lbl] = losses.mean()
        self.model.train()  # Set model back to train
        return out

    @staticmethod
    def self_attention():
        torch.manual_seed(1337)
        B, T, C = 4, 8, 32
        x = torch.randn(B, T, C)

        # # First approach is inefficient
        # xbow = torch.zeros((B, T, C))
        # for b in range(B):
        #     for t in range(T):
        #         xprev = x[b, :t+1]
        #         xbow[b, t] = torch.mean(xprev, 0)

        # # second approach uses vectorization to get parallel operations
        # weights = torch.tril(torch.ones(T, T))
        # weights = weights / weights.sum(1, keepdim=True)
        # xbow2 = weights @ x    # (B, T, T) @ (B, T, C) --> (B, T, C)
        # torch.allclose(xbow, xbow2)

        # # Third approach brings us nearer to attention mechanisms
        # tril = torch.tril(torch.ones(T, T))
        # weights = torch.zeros((T, T))
        # weights = weights.masked_fill(tril == 0, float('-inf'))
        # weights = F.softmax(weights, dim=1)
        # xbow3 = weights @ x
        '''
            At this point, we have weighted sums of all previous time slots
        '''

        #   Attention
        # Let's see a single head perform self-attention
        head_size = 16
        key = nn.Linear(C, head_size, bias=False)       # This is how you find this node
        query = nn.Linear(C, head_size, bias=False)     # This is the query for interesting nodes
                                                        # k.q is a vector of "interesting"
        value = nn.Linear(C, head_size, bias=False)     # This is the value for an interesting node

        k = key(x)      # (B, T, head_size)
        q = query(x)
        v = value(x)
        weights = q @ k.transpose(-2, -1)   # (B, T, head_size) @ (B, head_size, T) -> (B, T, T)

        tril = torch.tril(torch.ones(T, T))     # Only pay attention to nodes in the past
        weights = weights.masked_fill(tril == 0, float('-inf'))
        weights = F.softmax(weights, dim=1) * head_size**-0.5   # keeps softmax from getting to peaky
        out = weights @ v
