class Box:
    def __init__(self, top_left, box_size, frame_shape):
        # All positions and sizes are in (row, column) form
        self.frame_shape = frame_shape
        self.top = top_left[0]
        self.left = top_left[1]
        self.height = box_size[0]
        self.width = box_size[1]

    def top_left(self):
        return self.left, self.top

    def bottom_right(self):
        return self.left + self.width, self.top + self.height

    def move_one_pixel_down(self):
        self.top += 10
        if self.top + self.height > self.frame_shape[0]:
            self.top = 300

    def move_one_pixel_right(self):
        self.left += 10
        if self.left + self.width > self.frame_shape[1]:
            self.left = 300
