from datetime import datetime, timezone
import json

class SYSLOG:
    def __init__(self, echo=False, log=False, *args, **kwargs):
        if log:
            self.start_log(*args, **kwargs)
        self.log, self.echo = log, echo

    def start_log(self, folder=False, filepath=False):
        if folder and filepath:
            self.folder, self.filepath = folder, filepath
        else:
            self.log = False
            print('Logging was turned off, no folder or filepath.')

    def p(self, *args, **kwargs):
        line = [datetime.now().isoformat(sep=' T ', timespec='milliseconds'), *args, kwargs]
        if self.echo:
            print(*line)
        if self.log:
            self.append(line)       

    def append(self, data):
        with open(self.folder + self.filepath, 'a') as f:
            json.dump(data, f)
            f.write(',\n')

    def __call__(self, *args, **kwargs):
        if self.echo or self.log:
            self.p(*args, **kwargs)

class Mapping(dict):

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()
