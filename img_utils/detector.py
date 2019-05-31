import threading

import cv2

from config_utils.ConfigManager import *
from app_utils.functions import move_mouse, mouse_click, mute, play, next_track, vol_up, vol_down
from img_utils.imgprocessor import ImageProcessor

ALGO_SIMPLE = 0
ALGO_ADV = 1

debug_display = True


# model goes to model/output_graph.pb
# labels model/output_labels.txt
class Detector:
    def __init__(self):
        cam = cv2.VideoCapture(0)
        self.wait_complete = True
        self.ip = ImageProcessor(cam, 0.5)

        self.ip.attach_detector(self)
        self.config_manager = ConfigManager()

    def start(self, config):
        self.config_manager.load_config(config)
        self.ip.set_gesture_move(self.config_manager.get_mouse_move_gesture())
        self.ip.set_gesture_click(self.config_manager.get_mouse_click_gesture())

        self.ip.start_loop(ALGO_SIMPLE, display=debug_display)

    def on_gesture(self, gesture):
        if self.wait_complete:
            action = self.config_manager.get_action(gesture)
            try:
                if action == PLAY_PAUSE:
                    play()
                elif action == NEXT_TRACK:
                    next_track()
                elif action == MUTE:
                    mute()
                elif action == VOL_UP:
                    vol_up()
                elif action == VOL_DOWN:
                    vol_down()
                else:  # mouse move / mouse click / none
                    return
                self.wait_complete = False
                timer = threading.Timer(1.0, self.end_wait)
                timer.start()
            except TypeError:
                print(gesture)

    def end_wait(self):
        self.wait_complete = True
        print("wait over")

    @staticmethod
    def on_gesture_move(x_pos, y_pos):
        move_mouse(x_pos, y_pos)

    @staticmethod
    def on_gesture_click(x_pos, y_pos):
        mouse_click(x_pos, y_pos)


if __name__ == '__main__':
    detector = Detector()
    detector.start(None)
