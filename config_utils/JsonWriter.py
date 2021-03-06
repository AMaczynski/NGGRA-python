import json
from config_utils.JsonConfig import *

default_config = {GESTURE_THUMB: MUTE,
                  GESTURE_PEACE: NEXT_TRACK,
                  GESTURE_STRAIGHT: PLAY_PAUSE,
                  GESTURE_PALM: MOVE_MOUSE,
                  GESTURE_FIST: CLICK_MOUSE}


def save_config(filename, model):
    with open(filename, 'w') as f:
        json.dump(model, f, indent=4,
                  ensure_ascii=False)


if __name__ == "__main__":
    save_config("config.json", default_config)
