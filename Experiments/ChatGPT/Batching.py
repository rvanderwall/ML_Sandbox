import torch
from ChatGPT.Config import Config


class Batcher:
    def __init__(self, cfg: Config):
        torch.manual_seed(1337)
        self.device = cfg.device
        self.block_size = cfg.block_size
        self.batch_size = cfg.batch_size

    def get_batch(self, data):
        ix = torch.randint(len(data) - self.block_size, (self.batch_size,))
        x = torch.stack([data[i:i + self.block_size] for i in ix])
        y = torch.stack([data[i + 1:i + self.block_size + 1] for i in ix])
        x, y = x.to(self.device), y.to(self.device)
        return x, y

    def show_one_batch(self, data):
        xb, yb = self.get_batch(data)
        print(f'inputs:{xb.shape}')
        print(f'targets:{yb.shape}')
        print("--------------------")

        for b in range(4):
            for t in range(self.block_size):
                context = xb[b, :t + 1]
                target = yb[b, t]
                print(f"when input is {context.tolist()} the target is: {target}")
