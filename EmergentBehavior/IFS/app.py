import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from Visualization.GraphicPlayfield import GraphicPlayfield

# An Iterated Function System (IFS) is:
#   a set of linear maps (affine transforms)
#   associated set of probabilities
#   all maps have eigenvalues < 1
#
# W(x,y) = T * X + B
# T is a 2x2 transform matrix
#    [ a b ]
#    [ c d ]
#
# X is a 2x1 column vector
#
# B is a 2x1 offset
#   [ e
#     f ]
#
# W = [ ax + by + e
#       cx + dy + f ]

#   [   a,   b,   c,  d,    e,   f,    p]
Sierpinski_triangle = [
    [ 0.5, 0.0, 0.0, 0.5, 0.0, 0.0, 0.33],
    [ 0.5, 0.0, 0.0, 0.5, 1.0, 0.0, 0.33],
    [ 0.5, 0.0, 0.0, 0.5, 0.5, 0.5, 0.34],
]

fern = [
    [ 0.0,  0.0,   0.0,  0.16, 0.0, 0.0,  0.01],
    [ 0.2, -0.26,  0.23, 0.22, 0.0, 1.6,  0.07],
    [-0.15, 0.28,  0.26, 0.24, 0.0, 0.44, 0.07],
    [ 0.85, 0.04, -0.04, 0.85, 0.0, 1.6,  0.85],
]

square = [
    [ 0.5, 0.0, 0.0, 0.5, 0.0, 0.0, 0.25],
    [ 0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.25],
    [ 0.5, 0.0, 0.0, 0.5, 0.0, 0.5, 0.25],
    [ 0.5, 0.0, 0.0, 0.5, 0.5, 0.5, 0.25],
]

tree = [
    [ 0.0,   0.0,   0.0,  0.5,  0.0, 0.0, 0.05],
    [ 0.1,   0.0,   0.0,  0.1,  0.0, 0.2, 0.15],
    [ 0.42, -0.42,  0.42, 0.42, 0.0, 0.2, 0.40],
    [ 0.42,  0.42, -0.42, 0.42, 0.0, 0.2, 0.40],
]

# m1(z) = sz + 1
# m2(z) = sz - 1
# s = 0.33
cantor = [
    [ 0.33, 0.0, 0.0, 0.33,  1.0, 0, 0.5],
    [ 0.33, 0.0, 0.0, 0.33, -1.0, 0, 0.5]
]

# s = i/2 + 1/2
# sz = (i/2 + 1/2)(x + iy) = xi/2 + x/2 - y/2 + iy/2
#    = (x/2 - y/2) + (x/2 + y/2)i
dragon = [
    [0.5, -0.5, 0.5, 0.5,  1.5, 0, 0.5],
    [0.5, -0.5, 0.5, 0.5, -0.5, 0, 0.5]
]


""" Iterated Function System"""
class IFS:
    def __init__(self, W):
        self.NUM_ITERATIONS = 2500
        self.x = []
        self.y = []
        self.W = W
        self.last_x = 0
        self.last_y = 0

    def all_steps(self):
        x = 0
        y = 0
        for n in range(self.NUM_ITERATIONS):
            row = self.get_row(self.W)
            x, y = self.get_new_point(row, x, y)
            self.set_pixel(x, y)

    def step(self):
        # Run several iterations within each step
        for _ in range(100):
            row = self.get_row(self.W)
            self.last_x, self.last_y = self.get_new_point(row, self.last_x, self.last_y)
            self.set_pixel(self.last_x, self.last_y)

    def set_pixel(self, x, y):
        self.x.append(x)
        self.y.append(y)

    def get_row(self, W):
        pk = random.uniform(0, 1)
        for i in range(len(W)):
            row = W[i]
            p = row[6]
            if pk < p:
                return row
            pk -= p

        # Improperly formed W, probabilities should total 1.0
        return None

    def get_new_point(self, row, x, y):
        new_x = row[0] * x + row[1] * y + row[4]
        new_y = row[2] * x + row[3] * y + row[5]
        return new_x, new_y


ifs = None
points = None
class Animator:
    def __init__(self):
        pass

    @staticmethod
    def init():
        """initialize animation"""
        return

    @staticmethod
    def animate(i):
        # """perform animation step"""
        global ifs, points
        ifs.step()
        # update pieces of the animation
        points.set_data(ifs.x, ifs.y)
        return

    def run(self, rules):
        global ifs, points
        ifs = IFS(rules)
        size = 0.005
        bounds = [-2, 2, -2, 2]
        gpf = GraphicPlayfield(size, bounds)

        points, fig = gpf.build_graphic_playfield()

        ani = animation.FuncAnimation(fig, self.animate, frames=600,
                                      interval=10, blit=False, init_func=self.init)
        plt.show()


if __name__ == "__main__":
    a = Animator()
    a.run(dragon)
