import cv2

from FunctionManager import *
from imgprocessor import ImageProcessor

ALGO_SIMPLE = 0
ALGO_ADV = 1

debug_display = True
mouse_control = True


# model goes to model/output_graph.pb
# labels model/output_labels.txt
class Detector:
    def __init__(self):
        cam = cv2.VideoCapture(0)
        self.ip = ImageProcessor(cam, 0.5)
        if mouse_control:
            self.ip.enable_mouse_control()
            self.ip.set_gesture_move(PALM)
            self.ip.set_gesture_click(FIST)

        self.ip.attach_detector(self)
        self.function_manager = FunctionManager()

    def start(self, config):
        self.function_manager.load_config(config)
        self.ip.start_loop(ALGO_SIMPLE, display=debug_display)

    def on_gesture(self, gesture):
        try:
            self.function_manager.fun_dictionary.get(gesture)()
        except TypeError:
            print(gesture)

    def on_gesture_move(self, x_pos, y_pos):
        move_mouse(x_pos, y_pos)

    def on_gesture_click(self, x_pos, y_pos):
        mouse_click(x_pos, y_pos)


if __name__ == '__main__':
    detector = Detector()
    detector.start(None)
