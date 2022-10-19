import cv2
import argparse
from Video.Box import Box
from Video.VideoProcessor import VideoProcessor


class FaceFinder:
    def __init__(self, face_cascade: cv2.CascadeClassifier, eyes_cascade: cv2.CascadeClassifier):
        self.face_cascade = face_cascade
        self.eyes_cascade = eyes_cascade

    def detectAndDisplay(self, frame):
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(frame_gray)

        #  -- Detect faces --
        faces = self.face_cascade.detectMultiScale(frame_gray)
        for (x,y, w, h) in faces:
            center = (x + w//2, y + h//2)
            frame = cv2.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)

            faceROI = frame_gray[y:y+h, x:x+w]
            eyes = self.eyes_cascade.detectMultiScale(faceROI)
            for (x2, y2, w2, h2) in eyes:
                eye_center = (x + x2 + w2//2, y + y2 + h2//2)
                radius = int(round((w2 + h2) * 0.25))
                frame = cv2.circle(frame, eye_center, radius, (255, 0, 0), 4)
        cv2.imshow('Capture - Face detection', frame)


def parse_args():
    # https://github.com/opencv/opencv/tree/master/data/haarcascades
    parser = argparse.ArgumentParser(description='Code for Cascade Classifier')
    data_folder = "/Users/rvanderwall/projects/python/ML/Experiments/Video/data/haarcascades"
    parser.add_argument('--face_cascade', help='Path to face cascade',
                        default=f'{data_folder}/haarcascade_frontalface_alt.xml')
    parser.add_argument('--eyes_cascade', help='Path to eyes cascade.',
                        default=f'{data_folder}/haarcascade_eye_tree_eyeglasses.xml')
    parser.add_argument('--camera', help='Camera divide number', type=int, default=0)
    args = parser.parse_args()

    face_cascade_name = args.face_cascade
    face_cascade = cv2.CascadeClassifier()
    if not face_cascade.load(cv2.samples.findFile(face_cascade_name)):
        print('--(!)Error loading face cascade')
        exit(1)

    eyes_cascade_name = args.eyes_cascade
    eyes_cascade = cv2.CascadeClassifier()
    if not eyes_cascade.load(cv2.samples.findFile(eyes_cascade_name)):
        print('--(!)Error loading eyes cascade')
        exit(1)

    return face_cascade, eyes_cascade


def main2():
    print("face detection")
    face_cascade, eyes_cascade = parse_args()
    ff = FaceFinder(face_cascade, eyes_cascade)
    with VideoProcessor(save_to_file=False) as vp:
        while True:
            rc = vp.get_frame()
            if rc:
                ff.detectAndDisplay(vp.cur_frame)

            if cv2.waitKey(10) == 27:
                break


def main():
    print("video processing")
    with VideoProcessor(save_to_file=False) as vp:
        grab_size = (200, 200)
        grab = Box((280, 330), grab_size, vp.frame_shape)
        place = Box((0, 0), grab_size, vp.frame_shape)

        while True:
            rc = vp.get_frame()
            if rc:
                vp.mirror_frame()

                # grab.move_one_pixel_down()
                grab.move_one_pixel_right()
                eye = vp.crop_frame(grab)
                vp.write_pane(eye, place)

                # box.move_one_pixel_down()
                vp.add_box(grab.top_left(), grab.bottom_right())
                vp.add_text("capture", grab.bottom_right())

                cv2.imshow('frame', vp.cur_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main2()
