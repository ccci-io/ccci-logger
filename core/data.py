import time
import json
from datetime import datetime


class DataBank:
    hanged = {}     # 'action': 0
    datafile = {}

    # Set folder
    def __init__(self, folder):
        self.folder = folder

    # GET *.key
    def __getattr__(self, key):
        return self.datafile[key]

    # SET *.key
    def __setattr__(self, key, item):
        self.setting[key] = item

    # GET *[key]
    def __getitem__(self, key):
        return self.datafile[key]

    # SET *[key]
    def __setitem__(self, key, item):
        self.setting[key] = item

    # Get dictionary from json datafile.
    def __repr__(self):
        return repr(self.datafile)

    # *.('filepath')                /// Load settings from filepath
    def __call__(self, *args, **kwargs):
        return self.load(*args, **kwargs)

    # *.read('filepath')            /// Read file from filepath
    def read(self, filepath):
        with open(self.folder + filepath) as f:
            return json.load(f)

    # *.write('filepath', [data])   /// Overwrite file with data
    def write(self, filepath, data):
        with open(self.folder + filepath, 'w') as f:
            json.dump(data, f, indent=4)

    # *.append('filepath', [data])  /// Append data to file
    def append(self, filepath, data):
        with open(self.folder + filepath, 'a') as f:
            json.dump(data, f)
            f.write(',\n')

    # *.load('filepath')    /// Load dictionary from json file
    def load(self, filepath):
        self.datafile = self.read(filepath)
        self.datafile_filepath = filepath
        return self.datafile

    # *.save('filepath')    /// Save dictionary to json file
    def save(self, filepath=False):
        if filepath:
            self.write(self.folder, filepath)
        else:
            self.write(self.folder, self.datafile_filepath)

    # Add filepath for logging
    def set_log(self, filepath):
        self.datafile['log_path'] = filepath
        return filepath

    # Log data to set_log(filepath)
    def log(self, **kwargs):
        self.append(self.datafile['log_path'], {
            'timestamp': int(time.time()),
            **kwargs,
        })

    # Log data with ISO date to set_log(filepath)
    def log_iso(self, **kwargs):
        self.append(self.datafile['log_path'], {
            'timestamp': datetime.now().isoformat(sep=' T ', timespec='milliseconds'),
            **kwargs,
        })

    ############# # # # BUTTON OPERATIONS # # # ##############
    
    # Hand a file
    def hang(self, action):
        if action not in self.hanged:
            self.hanged[action] = 0
        self.hanged[action] += 1
        return self.hanged[action]

    # Delete action from hanged
    def reset_hanged(self, action):
        if action in self.hanged:
            del self.hanged[action]

    ############# # # # STANDALONES # # # ##############

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

    def custom_round(self, fresh, stable, change=0.07, decimals=1):
        if abs(fresh - stable) > change:
            return round(fresh, decimals)
        else:
            return False

    #def __repr__(self):
    #    return json.dumps(self.flags)

class Remote(DataBank):

    def receive(self):
        return