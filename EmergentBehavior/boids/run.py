from p5 import setup, draw, size, background, run
import numpy as np
from boids.boid import Boid

width = 1000
height = 1000

flock = [Boid(*np.random.rand(2)*1000, width, height) for _ in range(30)]


def setup():
    # This happens once
    size(width, height)  # Instead of creating a canvas


def draw():
    # This happens every time
    background(30, 30, 47)

    for boid in flock:
        boid.show()
        boid.apply_behavior(flock)
        boid.update()
        boid.edges()


run()
