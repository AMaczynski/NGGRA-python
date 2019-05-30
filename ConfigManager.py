from JsonConfig import *


class ConfigManager:
    def __init__(self):
        self.fun_dictionary = {}
        self.has_mouse_control = False
        self.mouse_move_gesture = None
        self.mouse_click_gesture = None

    def load_config(self, config):
        for gesture, action in config:
            if action == PLAY_PAUSE:
                self.fun_dictionary[gesture] = PLAY_PAUSE
            elif action == NEXT_TRACK:
                self.fun_dictionary[gesture] = NEXT_TRACK
            elif action == MUTE:
                self.fun_dictionary[gesture] = MUTE
            elif action == VOL_UP:
                self.fun_dictionary[gesture] = VOL_UP
            elif action == VOL_DOWN:
                self.fun_dictionary[gesture] = VOL_DOWN
            elif action == MOVE_MOUSE:
                self.has_mouse_control = True
                self.mouse_move_gesture = gesture
                self.fun_dictionary[gesture] = MOVE_MOUSE
            elif action == CLICK_MOUSE:
                self.has_mouse_control = True
                self.mouse_click_gesture = gesture
                self.fun_dictionary[gesture] = CLICK_MOUSE
            elif action == NO_ACTION:
                print("Gesture %s None" % gesture)
                self.fun_dictionary[gesture] = None

    def get_action(self, gesture):
        return self.fun_dictionary[gesture]

    def does_have_mouse_control(self):
        return self.has_mouse_control

    def get_mouse_move_gesture(self):
        return self.mouse_move_gesture

    def get_mouse_click_gesture(self):
        return self.mouse_click_gesture

