import numpy as np


class Column:
    def __init__(self, abs_x, abs_y, loc_x, loc_y):
        self.abs_x = abs_x
        self.abs_y = abs_y
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.column_shape = (0, 0)
        self.stack = []

    def set_stack(self, bottom_layer, num_levels):
        column_shape = bottom_layer.shape
        stack = [bottom_layer]
        for level in range(1, num_levels):
            next_layer = 64 * np.random.rand(column_shape[0], column_shape[1])
            stack.append(next_layer)

        self.stack = stack
        self.column_shape = column_shape
        return self


def build_columns(frame):
    column_shape = (16, 16, 5)
    slide = 12
    locations = {}
    col_x = -1
    col_y = -1
    for x in range(0, frame.shape[0] - column_shape[0] + 1, slide):
        col_x += 1
        col_y = -1
        for y in range(0, frame.shape[1] - column_shape[1] + 1, slide):
            col_y += 1

            x_top = x + column_shape[0]
            y_top = y + column_shape[1]
            bottom_layer = frame[x:x_top, y:y_top]
            c = Column(x, y, col_x, col_y).set_stack(bottom_layer, column_shape[2])
            locations[(col_x, col_y)] = c

    print(f"Locations shape: {(col_x, col_y)}")
    return locations

