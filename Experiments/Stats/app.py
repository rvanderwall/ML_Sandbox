from math import exp, pow, factorial, sqrt
from Visualization.Visualizer import Visualizer
from Stats.mc_sim import get_list_of_randoms


def poisson(l, N):
    p = exp(-l) * pow(l, N) / factorial(N)
    return p


def plot_poisson(v):
    print("Start stats")
    lamb = 3
    x = range(10)
    y = [poisson(lamb, xx) for xx in x]
    print("Visualize")
    v.visualize_data_bar("Poisonn", x, y, 0.3)


def n(x, alpha):
    return x / sqrt(x * x + alpha)


def plot_vader(v):
    x = range(1000)
    alpha = 1.0
    y = [n(xx / 1000.0, alpha) for xx in x]
    print(y)
    v.visualize_data_bar("Alpha", x, y, 1.00)


def run():
    v = Visualizer()
    plot_poisson(v)
    plot_vader(v)

if __name__ == "__main__":
    # run()
    get_list_of_randoms()
