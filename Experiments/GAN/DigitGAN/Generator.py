from torch import nn


class Generator(nn.Module):
    def __init__(self, shape):
        super().__init__()
        self.shape = shape
        self._input_size = shape[0] * shape[1]
        self.latent_space_dimensions = 100
        self.model = nn.Sequential(
            nn.Linear(self.latent_space_dimensions, 256),
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Linear(512, 1024),
            nn.ReLU(),
            nn.Linear(1024, self._input_size),
            nn.Tanh(),
        )

    def forward(self, x):
        output = self.model(x)
        output = output.view(x.size(0), 1, self.shape[0], self.shape[1])
        return output
