import cv2
from Video.Box import Box


class VideoProcessor:
    def __init__(self, save_to_file):
        self.video_stream = cv2.VideoCapture(0)

        if not self.video_stream.isOpened():
            print("Error opening camera")
            exit(1)

        width = int(self.video_stream.get(3))
        height = int(self.video_stream.get(4))
        self.frame_shape = (height, width)
        self.cur_frame = None
        print(f"Shape: {self.frame_shape}")      # Row, Col

        if save_to_file:
            camera_size = (width, height)  # X, Y --> For Video
            self.writer = cv2.VideoWriter('output.avi',
                                          cv2.VideoWriter_fourcc(*'MJPG'),
                                          10, camera_size)
        else:
            self.writer = None

    def get_frame(self):
        rc, frame = self.video_stream.read()
        if rc:
            self.cur_frame = frame
        return rc

    def get_info(self):
        bgr_pixel = self.cur_frame[100, 100]  # Grab a pixel from row, col
        red_pixel = self.cur_frame.item(100, 100, 2)  # faster
        shape = self.cur_frame.shape  # Shape is (rows, cols)

    def mirror_frame(self):
        self.cur_frame = cv2.flip(self.cur_frame, 1)  # 0-> vertically, 1->horizontally, 2->both

    def grey_scale(self):
        self.cur_frame = cv2.cvtColor(self.cur_frame, cv2.COLOR_BGR2GRAY)

    def crop_frame(self, box: Box):
        top = box.top
        bottom = top + box.height
        left = box.left
        right = left + box.width
        crop = self.cur_frame[top:bottom, left:right]
        return crop

    def write_pane(self, image, box: Box):
        top = box.top
        bottom = top + box.height
        left = box.left
        right = left + box.width
        self.cur_frame[top:bottom, left:right] = image

    def add_box(self, top_left, bottom_right):
        color = (0, 255, 0)
        line_width = 4
        self.cur_frame = cv2.rectangle(self.cur_frame, top_left, bottom_right, color, line_width)

    def add_text(self, text, position):
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 4
        font_color = (255, 255, 255)
        font_thickness = 2
        font_type = cv2.LINE_AA
        self.cur_frame = cv2.putText(self.cur_frame, text, position,
                                     font, font_size, font_color, font_thickness, font_type)

    def write_frame(self):
        if self.writer is not None:
            self.writer.write(self.cur_frame)

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        self.video_stream.release()
        if self.writer is not None:
            self.writer.release()
