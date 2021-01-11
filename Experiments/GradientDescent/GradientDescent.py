from typing import List
from random import randint

import plotly.graph_objects as go

# https://plotly.com/python/


class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def scale(self, scale):
        self.x *= scale
        self.y *= scale

    def __add__(self, other):
        p: Point = Point(self.x, self.y)
        p.x += other.x
        p.y += other.y
        return p

    def __str__(self):
        return f"x: {self.x}, y: {self.y}"


def paraboloid(p: Point) -> float:
    return p.x ** 2 + p.y ** 2


def compute_gradient(vec: Point) -> Point:
    return Point(2 * vec.x, 2 * vec.y)


def compute_step(curr_pos: Point, learning_rate: float) -> Point:
    grad: Point = compute_gradient(curr_pos)
    grad.scale(-learning_rate)
    next_pos: Point = curr_pos + grad
    return next_pos


def gradient_descent():
    start: Point = Point(randint(-10, 11), randint(-10, 11))
    epochs: int = 5000
    learning_rate: float = 0.001
    best_pos: Point = start

    for i in range(0, epochs):
        next_pos: Point = compute_step(best_pos, learning_rate)
        if i % 500 == 0:
            print(f"Epoch {i}: {next_pos}")
        best_pos = next_pos
    print(f'Best minimum: {best_pos}')


def generate_sample() -> (List[float], List[float], List[List[float]]):
    xs_start = ys_start = -10
    xs_stop = ys_stop = 11
    xs_step = ys_step = 1
    xs: List[float] = [i for i in range(xs_start, xs_stop, xs_step)]
    ys: List[float] = [i for i in range(ys_start, ys_stop, ys_step)]
    zs: List[List[float]] = []

    for x in xs:
        temp_res: List[float] = []
        for y in ys:
            result: float = paraboloid(Point(x, y))
            temp_res.append(result)
        zs.append(temp_res)
    return xs, ys, zs


def main():
    xs, ys, zs = generate_sample()
    print(f'xs: {xs}')
    fig = go.Figure(go.Surface(x=xs, y=ys, z=zs, colorscale='Viridis'))
    fig.show()
    gradient_descent()
    print("Hello")


if __name__ == "__main__":
    main()
