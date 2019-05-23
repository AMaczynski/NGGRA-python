import json
from JsonConfig import *

default_config = {THUMB: MUTE,
                  PEACE: NEXT_TRACK,
                  STRAIGHT: PLAY_PAUSE,
                  PALM: MOVE_MOUSE,
                  FIST: CLICK_MOUSE}


def save_config(filename, model):
    with open(filename, 'w') as f:
        json.dump(model, f, indent=4,
                  ensure_ascii=False)


if __name__ == "__main__":
    save_config("config.json", default_config)
