#!/usr/bin/env python3

import board
import busio
import json

from adafruit_si7021 import SI7021
from display import I2C_OLED
from bank import DataBank

def beep(boop):
    if boop:
        return False
    else:
        return True

def check(task):
    alert = data.alerts[task]
    flag = data.flags[task]
    value = data.sensors[alert['furnace']['sensor']]

    if flag['on']:
        boo = False
    else:
        boo = True

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


def monitor():
    #boop = data.flags['boop']
    #boop = beep(boop)
    oled.temperature(sensor.temperature)

    print(f"\nTemperature: {round(sensor.temperature, 2)} C")
    print(f"Humidity: {round(sensor.relative_humidity, 2)} %")
    print(data.flags)

    data.sensors = {
        'temperature': round(sensor.temperature, 2),
        'humidity': round(sensor.relative_humidity, 2),
    }

def operate():
    check('furnace')
    log(data)

folder = (__file__)[0:-13]

i2c = busio.I2C(board.SCL, board.SDA)   # Create library object using Adafruit Bus I2C port
sensor = SI7021(i2c)
oled = I2C_OLED(128, 64, i2c, folder)
data = DataBank(folder)