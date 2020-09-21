# CREATE A DEBUG/TEST/SYSTEM LOG

from datetime import datetime, timezone

class SYSLOG:
    def __init__(self, folder, filepath=False, log=False, echo=False):
        if not filepath:
            log = False
                    
        self.folder, self.filepath = folder, filepath
        self.log, self.echo = log, echo

    def p(self, value):
        line = [datetime.now().isoformat(sep=' T ', timespec='milliseconds'), value]
        if self.echo:
            print(*line)
        if self.log:
            self.append(line)

    def append(self, data):
        with open(self.folder + self.filepath, 'a') as f:
            json.dump(data, f)
            f.write(',\n')