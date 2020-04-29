#!/usr/bin/env python3

import board
import busio
import digitalio

from adafruit_si7021 import SI7021
#local
from display import I2C_OLED
from bank import DataBank
from panel import SwitchBoard


def check(task):

    alert = data.alerts[task]
    flag = data.flags[task]
    value = data.sensors[alert['sensor']]

    boo = not flag['on']

    if boo:                             # If furnace is [off]
        arg = value < alert['on']       # TRUE if colder than [on] alert
    else:                               # If furnace is [on]
        arg = value > alert['off']      # TRUE if warmer than [off] alert

    if alert['on'] > alert['off']:      # Correction for air conditioning
        arg = not arg

    if arg:
        if flag['check'] == boo:
            flag['on'] = boo
            sb.turn(task, boo) #sb.io[task].value = boo
        else:
            flag['check'] = boo
    else:
        flag['check'] = not boo


def respond(frequency=0.2, test=False):

    if sb.button:
        print(sb.button)

    return frequency


def monitor(frequency=1, test=False):

    data.sensors['temperature'] = round(sensor.temperature, 2)
    data.sensors['humidity'] = round(sensor.relative_humidity, 2)

    oled.show()
    #oled.large('temperature', sensor.temperature, '°')
    #oled.large('temperature', sensor.relative_humidity, '°')

    if True:
        print(f"\nTemperature: {round(sensor.temperature, 2)} C")
        print(f"Humidity: {round(sensor.relative_humidity, 2)} %")
        print(data.flags)

    return frequency


def operate(frequency=30, test=False):

    check('furnace')
    data.log()

    return frequency

folder = (__file__)[0:-13]

i2c = busio.I2C(board.SCL, board.SDA)   # Adafruit Bus I2C port library
sensor = SI7021(i2c)                    # Adafruit library for SI7021 sensor
data = DataBank(folder)
oled = I2C_OLED(128, 64, i2c, folder, data)   # Object that handles display
sb = SwitchBoard()
