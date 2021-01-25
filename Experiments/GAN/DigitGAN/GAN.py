import os

import torch
from torch import nn

from Experiments.GAN.GenericGAN.GenericGAN import GenericGAN

# https://realpython.com/generative-adversarial-networks/
class GAN(GenericGAN):
    def __init__(self, logger, train_data_set, discriminator, generator, visualizer, device):
        super().__init__(logger, train_data_set, discriminator, generator, visualizer)
        self.latent_dim = self._generator.latent_space_dimensions
        self.model_path = "Models"
        self.g_model_path = os.path.join(self.model_path, f"G_Model_{str(self.latent_dim)}.mdl")
        self.d_model_path = os.path.join(self.model_path, f"D_Model_{str(self.latent_dim)}.mdl")
        self.device = device

        self.batch_size = 32
        self.d_lr = 0.0001
        self.g_lr = 0.0001
        self.num_epochs = 10

        self._train_loader = torch.utils.data.DataLoader(
            self._train_set, batch_size=self.batch_size, shuffle=True
        )

    def show_training_data(self):
        real_samples, mnist_labels = next(iter(self._train_loader))
        samples = []
        for i in range(16):
            samples.append(real_samples[i])
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
        self._optimizer_discriminator = torch.optim.Adam(self._discriminator.parameters(), lr=self.d_lr)
        self._optimizer_generator = torch.optim.Adam(self._generator.parameters(), lr=self.g_lr)
        for epoch in range(self.num_epochs):
            self._run_epoch(epoch, verbose)

    def _run_epoch(self, epoch, verbose):
        last_batch_num = len(self._train_loader.dataset) // self.batch_size
        for batch_num, (real_samples, mnist_labels) in enumerate(self._train_loader):
            # Run one batch ...
            # self.logger.log(f"Epoch:{epoch}, Batch:{batch_num}, num_samples:{len(real_samples)}")
            # self.v.visualize_data_img("MNIST Samples", real_samples)

            # Data for training the discriminator
            real_samples = real_samples.to(device=self.device)
            real_samples_labels = torch.ones((self.batch_size, 1)).to(device=self.device)
            latent_space_samples = torch.randn((self.batch_size, self.latent_dim)).to(device=self.device)
            generated_samples = self._generator(latent_space_samples)
            generated_samples_labels = torch.zeros((self.batch_size, 1)).to(device=self.device)
            all_samples = torch.cat((real_samples, generated_samples))
            all_samples_labels = torch.cat((real_samples_labels, generated_samples_labels))

            # Training the discriminator
            self._discriminator.zero_grad()
            output_discriminator = self._discriminator(all_samples)
            loss_discriminator = self._loss_function(
                output_discriminator, all_samples_labels)
            loss_discriminator.backward()
            self._optimizer_discriminator.step()

            # Data for training the generator
            latent_space_samples = torch.randn((self.batch_size * 2, self.latent_dim)).to(device=self.device)
            generated_samples = self._generator(latent_space_samples)
            generated_samples_labels = torch.ones((self.batch_size * 2, 1)).to(device=self.device)

            # Training the generator
            self._generator.zero_grad()
            output_discriminator_generated = self._discriminator(generated_samples)
            loss_generator = self._loss_function(
                output_discriminator_generated, generated_samples_labels
            )
            loss_generator.backward()
            self._optimizer_generator.step()
            batch_num += 1

            # Show loss
            if batch_num == last_batch_num-1 or batch_num % 100 == 0:
                msg = f"Epoch: {epoch}, Batch: {batch_num}, Loss D: {loss_discriminator} Loss G.: {loss_generator}"
                self.logger.log(msg)

            if verbose and epoch % 2 == 0 and (batch_num == last_batch_num-1 or batch_num % 2000 == 0):
                self.show_generated_sample()
