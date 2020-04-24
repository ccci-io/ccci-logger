#!/usr/bin/env python3

import board
import busio
import json

from adafruit_si7021 import SI7021
from adafruit_ssd1306 import SSD1306_I2C

from display import I2C_OLED

def beep(boop):
    if boop:
        return False
    else:
        return True

def read_settings():
    with open(folder + 'json/settings.json') as f:
        return json.load(f)

def write_settings(settings):
    with open(folder + 'json/settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

def log_data(data):
    with open(folder + 'json/log.json', 'a') as f:
        log = {
            'ts': int(time.time()),
            'sensors': data['sensors'],
            'flags': data['flags'],
        }
        json.dump(log, f)
        f.write(',\n')

def check(data, value, task, boo):
    alert = data['alert'][task]
    flag = data['flag'][task]

    if boo:                             # If furnace is [off]
        arg = value < alert['on']       # TRUE if colder than [on] alert
    else:                               # If furnace is [on]
        arg = value > alert['off']      # TRUE if warmer than [off] alert

    if alert['on'] > alert['off']:      # Correction for air conditioning
        arg = beep(arg)

    if arg:
        if flag['check'] == boo:
            flag['on'] = boo
        else:
            flag['check'] = boo
    else:
        flag['check'] = beep(boo)

#async def print_after(flag, temp, delay):
#    print('30 SECOND DELAY STARTED')
#    await asyncio.sleep(delay)
#    print('Temp Check')

#async def print_after(flag, temp, delay):
#    print('30 SECOND DELAY STARTED')
#    await asyncio.sleep(delay)
#    print('Temp Check')

def monitor():
    boop = data['flags']['boop']
    boop = beep(boop)
    oled.temperature(sensor.temperature)

    print(f"\nTemperature: {round(sensor.temperature, 2)} C")
    print(f"Humidity: {round(sensor.relative_humidity, 2)} %")

    data['sensors'] = {
        'temp': round(sensor.temperature, 2),
        'humidity': round(sensor.relative_humidity, 2),
    }

def operate():
    if data['flags']['furnace']['on']:
        check(data, data['sensors']['temp'], 'furnace', False)
    else:
        check(data, data['sensors']['temp'], 'furnace', True)
    log_data(data)

folder = (__file__)[0:-13]

boop = False

i2c = busio.I2C(board.SCL, board.SDA)   # Create library object using Adafruit Bus I2C port
sensor = SI7021(i2c)
oled = I2C_OLED(128, 64, i2c, '/home/pi/ccci-controller/')
disp = SSD1306_I2C(128, 64, i2c)   # Pixel width and height.

data = {
    'alerts': read_settings(),
    'flags': {
        'furnace': {
            'check': False,
            'on': False,
        },
        'boop': False,
    },
    'sensors': {
        'temp': 0,
        'humidity': 0,
    },
}

data['sensors']['temp'] = data['alerts']['furnace']['off']
