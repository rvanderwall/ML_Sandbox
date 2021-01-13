import os

import torch
from torch import nn

from Experiments.GAN.GenericGAN.GenericGAN import GenericGAN


class GAN(GenericGAN):
    '''
        Create a batch
            r real values labeled 1
            B-r generated values labeled 0
        Loss = sum((Y-label)^2)
        train Discriminator to minimize loss
            trains to tell real from fake

        Freeze D
        G --> D   Loss=sum((1-Y)^2)
        Train G to minimize loss
            trains to generate better fakes
    '''
    def __init__(self, logger, train_data_set, discriminator, generator, visualizer):
        super().__init__(logger, train_data_set, discriminator, generator, visualizer)
        self.latent_dim = self._generator.latent_space_dimensions
        self.model_path = "Models"
        self.g_model_path = os.path.join(self.model_path, f"G_Model_{str(self.latent_dim)}.mdl")
        self.d_model_path = os.path.join(self.model_path, f"D_Model_{str(self.latent_dim)}.mdl")

        self.batch_size = 32
        self.lr = 0.001
        self.num_epochs = 300

    def show_training_data(self):
        X = [row[0].data[0].item() for row in self._train_set]
        Y = [row[0].data[1].item() for row in self._train_set]
        self.v.visualize_data_scatter("FuncGAN", X, Y, 1.1)

    def show_generated_sample(self):
        num_points = 200
        latent_space_samples = torch.randn(num_points, self.latent_dim)

        print(f"Shape of latent space samples: {latent_space_samples.shape}")
        generated_samples = self._generator(latent_space_samples)
        generated_samples = generated_samples.detach()
        X = generated_samples[:, 0]
        Y = generated_samples[:, 1]
        self.v.visualize_data_scatter("FuncGAN Generator", X, Y, 1.5)

    def train(self, verbose=False):
        self._train_loader = torch.utils.data.DataLoader(
            self._train_set, batch_size=self.batch_size, shuffle=True
        )
        self._loss_function = nn.BCELoss()
        self._optimizer_discriminator = torch.optim.Adam(self._discriminator.parameters(), lr=self.lr)
        self._optimizer_generator = torch.optim.Adam(self._generator.parameters(), lr=self.lr)
        for epoch in range(self.num_epochs):
            self._run_epoch(self.batch_size, epoch, verbose)

    def _run_epoch(self, batch_size, epoch, verbose):
        for n, (real_samples, _) in enumerate(self._train_loader):
            # Run one batch ...
            # Data for training the discriminator
            real_samples_labels = torch.ones((batch_size, 1))
            latent_space_samples = torch.randn((batch_size, self.latent_dim))
            generated_samples = self._generator(latent_space_samples)
            generated_samples_labels = torch.zeros((batch_size, 1))
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
            latent_space_samples = torch.randn((batch_size, self.latent_dim))

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
            if epoch % 10 == 0 and n == batch_size - 1:
                print(f"Epoch: {epoch} Loss D.: {loss_discriminator}")
                print(f"Epoch: {epoch} Loss G.: {loss_generator}")

            if verbose and epoch % 50 == 0 and n == batch_size -1:
                self.show_generated_sample()
