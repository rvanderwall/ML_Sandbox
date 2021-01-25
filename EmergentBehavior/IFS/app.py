import math
import random
from p5 import Vector, stroke, circle

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

SCREEN_X = 350
SCREEN_Y = 325
x_offset = 0
y_offset = 0
NUM_ITERATIONS = 2500

def set_pixel(x, y):
    stroke(255)
    circle((x, y), radius=10)


def get_row(W):
    pk = random.uniform(0, 1)
    for i in range(len(W)):
        row = W[i]
        p = row[6]
        if pk < p:
            return row
        pk -= p

    # Improperly formed W, probabilities should total 1.0
    return None


def get_new_point(row, x, y):
    new_x = row[0] * x + row[1] * y + row[4]
    new_y = row[2] * x + row[3] * y + row[5]
    return new_x, new_y


def run():
    x = 0
    y = 0
    W = square
    for n in range(NUM_ITERATIONS):
        row = get_row(square)
        x, y = get_new_point(x, y, row)
        set_pixel(x, y)

if __name__ == "__main__":
    get_row(square)
