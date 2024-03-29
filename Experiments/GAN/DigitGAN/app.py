import torch

from Experiments.GAN.DigitGAN.DataSrc import DataSrc
from Experiments.GAN.DigitGAN.GAN import GAN
from Experiments.GAN.DigitGAN.Discriminator import Discriminator
from Experiments.GAN.DigitGAN.Generator import Generator

from Experiments.GAN.GenericGAN.Logger import Logger
from Experiments.Visualization.Visualizer import Visualizer

l = Logger()
l.log("Starting GAN app")

device = ""
if torch.cuda.is_available():
    device = torch.device("cuda")
    l.log("Using CUDA device")
else:
    device = torch.device("cpu")
    l.log("Using CPU device")

d = DataSrc(l)
shape = d.image_shape()
train_set = d.prep_training_data()
disc = Discriminator(shape).to(device=device)
gen = Generator(shape).to(device=device)
gan = GAN(l, train_set, disc, gen, Visualizer(), device)
gan.show_training_data()

if gan.model_exists():
    gan.restore_model()
else:
    gan.train(verbose=False)
    gan.save_model()

for i in range(10):
    gan.show_generated_sample()
