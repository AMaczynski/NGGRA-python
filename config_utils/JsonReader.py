import json


class Reader:
    def __init__(self):
        self.data = None

    def read_config(self, filename):
        with open(filename) as f:
            data = json.load(f)
        self.data = data

    def get_attribute(self, attribute):
        return self.data[attribute]
