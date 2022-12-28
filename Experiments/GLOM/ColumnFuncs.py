import numpy as np
from numpy.linalg import norm
from GLOM.Columns import Column


class Weights:
    def __init__(self):
        self.W_self = 0.35
        self.W_top_down = 0.25
        self.W_bottom_up = 0.15
        self.W_attention = 0.25


def cos_similarity(c1: Column, c2: Column, level: int):
    m1 = c1.stack[level]
    m2 = c2.stack[level]
    cos = 0.0
    for row in range(m1.shape[0]):
        cos += np.dot(m1[row, :], m2[row, :])
    cos = cos / (norm(m1) * norm(m2) * m1.shape[0])
    return cos


def add_attention(c: Column, locations, w: Weights):
    num_levels = len(c.stack)
    for level in range(1, num_levels):
        for k in locations:
            c2 = locations[k]
            d = cos_similarity(c, c2, level)
            attention = w.W_attention * d * c2.stack[level]
            c.stack[level] = attention + c.stack[level]
    return c


def iterate_column(c: Column, w: Weights):
    stack = c.stack
    for level in range(1, len(stack)):
        new_slice = w.W_self * np.copy(stack[level])
        if level > 0:
            new_slice += w.W_bottom_up * stack[level - 1]
        else:
            new_slice += w.W_bottom_up * stack[level]

        if level < len(stack) - 1:
            new_slice += w.W_top_down * stack[level + 1]
        else:
            new_slice += w.W_top_down * stack[level]

        stack[level] = new_slice

    c.stack = stack
    return c
