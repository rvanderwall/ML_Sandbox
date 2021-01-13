import math
from math import sin

from Experiments.GAN.FuncGAN.DataSrc import DataSrc
from Experiments.GAN.FuncGAN.GAN import GAN
from Experiments.GAN.FuncGAN.Discriminator import Discriminator
from Experiments.GAN.FuncGAN.Generator import Generator

from Experiments.GAN.GenericGAN.Logger import Logger
from Experiments.Visualization.Visualizer import Visualizer


def func_to_simulate(x):
    return sin(2 * math.pi * x)

l = Logger()
d = DataSrc()
train_set = d.prep_training_data(func_to_simulate)

gan = GAN(l, train_set, Discriminator(), Generator(), Visualizer())
# gan.show_training_data()

if gan.model_exists():
    gan.restore_model()
else:
    gan.train(verbose=True)
    gan.save_model()

gan.show_generated_sample()
