from JsonConfig import *


class ConfigManager:
    def __init__(self):
        self.fun_dictionary = {}

    def load_config(self, config):
        for gesture, action in config:
            if action == PLAY_PAUSE:
                self.fun_dictionary[gesture] = PLAY_PAUSE
            elif action == NEXT_TRACK:
                self.fun_dictionary[gesture] = NEXT_TRACK
            elif action == MUTE:
                self.fun_dictionary[gesture] = MUTE
            elif action == MOVE_MOUSE:
                self.fun_dictionary[gesture] = MOVE_MOUSE
            elif action == CLICK_MOUSE:
                self.fun_dictionary[gesture] = CLICK_MOUSE

    def get_action(self, gesture):
        return self.fun_dictionary[gesture]