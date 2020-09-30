import time
import json

class DataBank:
    hanged = {}     # 'action': 0
    settings = {}
    signal = {}

    def __getattr__(self, key):
        return self.settings[key]

    def __getitem__(self, key):
        return self.settings[key]

    def __init__(self, folder):
        self.folder = folder

    def __repr__(self):
        return repr(self.settings)

    def __call__(self, *args, **kwargs):
        return self.load_settings(*args, **kwargs)

    def read(self, filepath):
        with open(self.folder + filepath) as f:
            return json.load(f)

    def write(self, filepath, data):
        with open(self.folder + filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def append(self, filepath, data):
        with open(self.folder + filepath, 'a') as f:
            json.dump(data, f)
            f.write(',\n')

    def load_settings(self, filepath):
        self.settings = self.read(filepath)
        return self.settings

    def save_settings(self, filepath):
        self.write(filepath, self.settings)

    def hang(self, action):
        if action not in self.hanged:
            self.hanged[action] = 0
        self.hanged[action] += 1
        return self.hanged[action]

    def reset_hanged(self, action):
        if action in self.hanged:
            del self.hanged[action]

    def indexOf(self, dicts, key, value):
        for i, d in enumerate(dicts):
            if d[key] == value:
                return i

    def flag_check(self, case, switch, value):

        boo = not switch.value

        if boo:                             # If furnace is [off]
            arg = value < case['on']       # TRUE if colder than [on] alert
        else:                               # If furnace is [on]
            arg = value > case['off']      # TRUE if warmer than [off] alert

        if case['on'] > case['off']:      # Correction for air conditioning
            arg = not arg

        if arg:
            if case['flag'] == boo:
                switch.value = boo
            else:
                case['flag'] = boo
        else:
            case['flag'] = not boo


    #def __repr__(self):
    #    return json.dumps(self.flags)


class Remote(DataBank):

    def receive(self):
        return