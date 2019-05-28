import threading

import pyautogui

from JsonConfig import *


def calc_new_mouse_position(x_diff, y_diff, x_image_size):
    x_pos, y_pos = pyautogui.position()
    x_screen, y_screen = pyautogui.size()
    scale = x_screen / x_image_size
    x_pos = x_pos - x_diff * scale
    y_pos = y_pos + y_diff * scale
    return x_pos, y_pos


def move_mouse(x_pos, y_pos):
    pyautogui.moveTo(x_pos, y_pos)


def mouse_click(x, y):
    pyautogui.click(x, y)


class FunctionManager:

    def __init__(self):
        self.wait_complete = True
        self.fun_dictionary = {}

    def end_wait(self):
        self.wait_complete = True
        print("wait over")

    def play(self):
        if self.wait_complete:
            pyautogui.press("playpause")
            print("PLAY/PAUSE")
            self.wait_complete = False
            timer = threading.Timer(3.0, self.end_wait)
            timer.start()
        else:
            print("wait not over")

    def next_track(self):
        if self.wait_complete:
            pyautogui.press("nexttrack")
            print("NEXT TRACK")
            self.wait_complete = False
            timer = threading.Timer(3.0, self.end_wait)
            timer.start()
        else:
            print("wait not over")

    def mute(self):
        if self.wait_complete:
            pyautogui.press("volumemute")
            print("MUTE/UNMUTE")
            self.wait_complete = False
            timer = threading.Timer(3.0, self.end_wait)
            timer.start()
        else:
            print("wait not over")

    def load_config(self, config):
        for gesture, action in config:
            if action == PLAY_PAUSE:
                self.fun_dictionary[gesture] = self.play
            elif action == NEXT_TRACK:
                self.fun_dictionary[gesture] = self.next_track
            elif action == MUTE:
                self.fun_dictionary[gesture] = self.mute
            elif action == MOVE_MOUSE:
                self.fun_dictionary[gesture] = move_mouse
            elif action == CLICK_MOUSE:
                self.fun_dictionary[gesture] = mouse_click
