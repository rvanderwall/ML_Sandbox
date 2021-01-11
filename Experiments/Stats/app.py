from math import exp, pow, factorial, sqrt
from Experiments.Visualization.Visualizer import Visualizer


def poisson(l, N):
    p = exp(-l) * pow(l, N) / factorial(N)
    return p

def plot_poisson():
    print("Start stats")
    l = 3
    x = range(10)
    y = [poisson(l, xx) for xx in x]
    print("Visualize")
    v.visualize_data_bar("Poisonn", x, y, 0.3)

def n(x, alpha):
    return x / sqrt(x * x + alpha)

def plot_vader():
    x = range(1000)
    alpha = 1.0
    y = [n(xx / 1000.0, alpha) for xx in x]
    print(y)
    v.visualize_data_bar("Alpha", x, y, 1.00)


v = Visualizer()
# plot_poisson()
plot_vader()