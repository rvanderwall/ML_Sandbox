import random


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
