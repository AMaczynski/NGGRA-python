import cv2
from imgprocessor import ImageProcessor


ALGO_SIMPLE = 0
ALGO_ADV = 1

debug_display = True

# model goes to model/output_graph.pb
# labels model/output_labels.txt
class Detector:
    def __init__(self):
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FPS, 5)
        # ImageProcessor(cam reference, image scale)
        self.ip = ImageProcessor(cam, 0.5)

    def start(self):
        self.ip.start_loop(ALGO_SIMPLE, self, display=debug_display)

    def on_gesture(self, gesture):
        if gesture == "fist":
            print("fist")
        elif gesture == "palm":
            print("palm")

if __name__ == '__main__':
    detector = Detector()
    detector.start()
