from math import fabs
from cmath import sin, exp
import numpy as np


milliped = [(-80.5, 20.5), (-20.5, 20.5)]

class Generator():
    def __init__(self, grid_size):
        self.x_size = grid_size[0]
        self.y_size = grid_size[1]
        self.grid = np.zeros(grid_size)
        self.min_x = -30.5
        self.max_x = 20.5
        self.min_y = -20.5
        self.max_y = 20.5


    def fill_grid(self, ):
        for x in range(self.x_size):
            for y in range(self.y_size):
                self.grid[y][x] = self.get_point_value(x, y)

    def get_point_value(self, x, y):
        # z^3 + c
        z = self.scale(x, y)
        for n in range(10):
            z = self.calculate_z(z)
            if self.stop(z):
                break

        if fabs(z.real) < 10 or fabs(z.imag) < 10:
            return 0
        else:
            return 255

    def scale(self, x, y):
        x = self.min_x + (self.max_x - self.min_x) * x / self.x_size
        y = self.min_y + (self.max_y - self.min_y) * y / self.y_size
        return complex(x, y)

    def stop(self, z):
        if fabs(z.real) > 10:
            return True
        if fabs(z.imag) > 10:
            return True
        if (z * z.conjugate()).real > 100:
            return True
        return False

    # http://www.madteddy.com/biomorph.htm
    # https://www.jstor.org/stable/24988989?seq=1
    def calculate_z(self, z):
        c = 0.1 + 0.2j
        # z = z*z*z + c
        # z = z*z*z*z*z + c
        z = sin(z) + z * z + c
        # z = sin(z) + exp(z) + c
        return z
