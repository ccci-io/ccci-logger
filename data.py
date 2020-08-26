import time
import json

class DataBank:
    def __init__(self, folder):
        self.folder = folder
        self.alerts = self.read('settings') #DJANGO SERVER WILL REPLACE THIS!
        #self.update_alerts()
        self.flags = {
            'modem': {
                'on': False,
                'notified': False,
            },
        }
        self.sensors = {}

    def read(self, name):
        with open(f'{self.folder}json/{name}.json') as f:
            return json.load(f)

    def write(self, name, data):
        with open(f'{self.folder}json/{name}.json', 'w') as f:
            json.dump(data, f, indent=4)

    def append(self, name, data):
        with open(f'{self.folder}json/{name}.json', 'a') as f:
            json.dump(data, f)
            f.write(',\n')

    def update_alerts(self):
        self.alerts = self.read('settings')

    def log(self):
        data = {
            'ts': int(time.time()),
            'sensors': self.sensors,
            'flags': self.flags,
        }
        self.append('log', data)

    def __repr__(self):
        return json.dumps(self.flags)


class Remote(DataBank):

    def receive(self):
        return