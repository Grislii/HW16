import json


class JsonRead:
    def __init__(self, path):
        self.path = path

    def load_data(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            return json.load(file)
