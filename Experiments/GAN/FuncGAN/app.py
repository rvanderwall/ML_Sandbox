import math
from math import sin

from Experiments.GAN.FuncGAN.DataSrc import DataSrc
from Experiments.GAN.FuncGAN.GAN import GAN


def func_to_simulate(x):
    return sin(2 * math.pi * x )


d = DataSrc()
train_set = d.prep_training_data(func_to_simulate)
gan = GAN(train_set)
# gan.show_training_data()

if gan.model_exists():
    gan.restore_model()
else:
    gan.train(verbose=True)
    gan.save_model()

gan.show_generated_sample()

