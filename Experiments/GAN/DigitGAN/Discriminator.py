from torch import nn


class Discriminator(nn.Module):
    def __init__(self, shape):
        super().__init__()
        self.shape = shape
        self._input_size = shape[0] * shape[1]
        self.model = nn.Sequential(
            nn.Linear(self._input_size, 1024),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = x.view(x.size(0), self._input_size)
        output = self.model(x)
        return output
