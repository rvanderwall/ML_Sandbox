import os

import torch
from torch import nn

from Experiments.GAN.GenericGAN.GenericGAN import GenericGAN


class GAN(GenericGAN):
    def __init__(self, train_data_set, discriminator, generator, visualizer, device):
        super().__init__(train_data_set, discriminator, generator, visualizer)
        self.latent_dim = self._generator.latent_space_dimensions
        self.model_path = "Models"
        self.g_model_path = os.path.join(self.model_path, f"G_Model_{str(self.latent_dim)}.mdl")
        self.d_model_path = os.path.join(self.model_path, f"D_Model_{str(self.latent_dim)}.mdl")
        self.device = device

        self.batch_size = 32
        self.lr = 0.0001
        self.num_epochs = 50

        self._train_loader = torch.utils.data.DataLoader(
            self._train_set, batch_size=self.batch_size, shuffle=True
        )
        self.real_samples, self.mnist_labels = next(iter(self._train_loader))

    def show_training_data(self):
        samples = []
        for i in range(16):
            samples.append(self.real_samples[i])
        self.v.visualize_data_img("MNIST Samples", samples)

    def show_generated_sample(self):
        latent_space_samples = torch.randn(self.batch_size, 100).to(device=self.device)
        generated_samples = self._generator(latent_space_samples)
        generated_samples = generated_samples.cpu().detach()
        samples = []
        for i in range(16):
            samples.append(generated_samples[i])
        self.v.visualize_data_img("Generated Samples", samples)

    def train(self, verbose=False):
        self._loss_function = nn.BCELoss()
        self._optimizer_discriminator = torch.optim.Adam(self._discriminator.parameters(), lr=self.lr)
        self._optimizer_generator = torch.optim.Adam(self._generator.parameters(), lr=self.lr)
        for epoch in range(self.num_epochs):
            self._run_epoch(epoch, verbose)

    def _run_epoch(self, epoch, verbose):
        for n, (real_samples, _) in enumerate(self._train_loader):
            # Run one batch ...
            # Data for training the discriminator
            real_samples = self.real_samples.to(device=self.device)
            real_samples_labels = torch.ones((self.batch_size, 1)).to(device=self.device)
            latent_space_samples = torch.randn((self.batch_size, self.latent_dim)).to(device=self.device)
            generated_samples = self._generator(latent_space_samples)
            generated_samples_labels = torch.zeros((self.batch_size, 1)).to(device=self.device)
            all_samples = torch.cat((real_samples, generated_samples))
            all_samples_labels = torch.cat(
                (real_samples_labels, generated_samples_labels)
            )

            # Training the discriminator
            self._discriminator.zero_grad()
            output_discriminator = self._discriminator(all_samples)
            loss_discriminator = self._loss_function(
                output_discriminator, all_samples_labels)
            loss_discriminator.backward()
            self._optimizer_discriminator.step()

            # Data for training the generator
            latent_space_samples = torch.randn((self.batch_size, self.latent_dim)).to(device=self.device)

            # Training the generator
            self._generator.zero_grad()
            generated_samples = self._generator(latent_space_samples)
            output_discriminator_generated = self._discriminator(generated_samples)
            loss_generator = self._loss_function(
                output_discriminator_generated, real_samples_labels
            )
            loss_generator.backward()
            self._optimizer_generator.step()

            # Show loss
            if n == self.batch_size - 1:
                print(f"Epoch: {epoch} Loss D.: {loss_discriminator}")
                print(f"Epoch: {epoch} Loss G.: {loss_generator}")

            if verbose and epoch % 2 == 0 and n == self.batch_size -1:
                self.show_generated_sample()
