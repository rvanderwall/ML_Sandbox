import os
from abc import ABC, abstractmethod
import torch


class GenericGAN(ABC):
    def __init__(self, train_data_set, discriminator, generator, visualizer):
        self._train_set = train_data_set
        self._discriminator = discriminator
        self._generator = generator
        self.v = visualizer
        self.model_path = "Models"
        self.g_model_path = None
        self.d_model_path = None

    def save_model(self):
        torch.save(self._generator.model.state_dict(), self.g_model_path)
        torch.save(self._discriminator.model.state_dict(), self.d_model_path)

    def model_exists(self):
        return os.path.exists(self.g_model_path)

    def restore_model(self):
        self._generator.model.load_state_dict(torch.load(self.g_model_path))
        self._generator.model.eval()
        self._discriminator.model.load_state_dict(torch.load(self.d_model_path))
        self._discriminator.model.eval()

    @abstractmethod
    def show_training_data(self):
        pass

    @abstractmethod
    def show_generated_sample(self):
        pass

    @abstractmethod
    def train(self, verbose=False):
        pass

