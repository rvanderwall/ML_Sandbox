import torch
from torch import nn


class Generator(nn.Module):
    def __init__(self):
        self.latent_space_dimensions = 2
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(self.latent_space_dimensions, 16),
            nn.ReLU(),
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, 2),
        )

    def forward(self, x):
        output = self.model(x)
        return output
