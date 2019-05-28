import wmi as wmi
import pyautogui
import threading
from JsonConfig import *

# def speakers_mute():
#     sessions = AudioUtilities.GetAllSessions()
#     for session in sessions:
#         volume = session.SimpleAudioVolume
#         if session.Process and session.Process.name() == "chrome.exe":
#             volume.SetMute(0, None)
#         else:
#             volume.SetMute(1, None)
#
#
# def speakers_change_volume_level(mode):
#     if mode == 1:
#         changeLevel = 0.1
#     else:
#         changeLevel = -0.1
#
#     sessions = AudioUtilities.GetAllSessions()
#     for session in sessions:
#         volume = session._ctl.QueryInterface(ISimpleAudioVolume)
#         if session.Process and session.Process.name() == "chrome.exe":
#             volume.SetMasterVolume(volume.GetMasterVolume() + changeLevel, None)


def change_brightness(brightness_level):
    wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(brightness_level, 0)


def move_mouse(x_diff, y_diff, x_image_size):
    x_pos, y_pos = pyautogui.position()
    x_screen, y_screen = pyautogui.size()
    scale = x_screen / x_image_size
    x_pos = x_pos - x_diff * scale
    y_pos = y_pos + y_diff * scale
    pyautogui.moveTo(x_pos, y_pos)

    return x_pos, y_pos


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
