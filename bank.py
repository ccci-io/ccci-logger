import time
import json

class DataBank:
    def __init__(self, folder):
        self.folder = folder
        self.alerts = self.read('settings')
        #self.update_alerts()
        self.flags = {
            'furnace': {
                'check': False,
                'on': False,
            },
        }
        self.sensors = {
            'temperature': self.alerts['furnace']['off'],
            'humidity': 0,
        }

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


class Remote(DataBank):

    def receive(self):
        return