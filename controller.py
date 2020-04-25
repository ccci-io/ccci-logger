#!/usr/bin/env python3

import board
import busio
import digitalio
 
from adafruit_si7021 import SI7021
from display import I2C_OLED
from bank import DataBank

def check(task):
    alert = data.alerts[task]
    flag = data.flags[task]
    value = data.sensors[alert['sensor']]
    print(alert)
    print(flag)

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
            #switchboard(task, boo)
        else:
            flag['check'] = boo
    else:
        flag['check'] = not boo

# Switch digital output
def switchboard(task, boo):
    gpio[task].value = boo

# Assign digital output
def digital_output(task, pin):
    gpio[task] = digitalio.DigitalInOut(pin)
    gpio[task].direction = digitalio.Direction.OUTPUT

# Assign digital input
def digital_input(task, pin):
    gpio[task] = digitalio.DigitalInOut(pin)
    gpio[task].direction = digitalio.Direction.INPUT
    gpio[task].pull = digitalio.Pull.UP

def monitor():

    oled.temperature(sensor.temperature)

    print(f"\nTemperature: {round(sensor.temperature, 2)} C")
    print(f"Humidity: {round(sensor.relative_humidity, 2)} %")
    print(data.flags)

    data.sensors['temperature'] = round(sensor.temperature, 2)
    data.sensors['humidity'] = round(sensor.relative_humidity, 2)
    
def operate():
    check('furnace')
    data.log()

folder = (__file__)[0:-13]

i2c = busio.I2C(board.SCL, board.SDA)   # Create library object using Adafruit Bus I2C port
sensor = SI7021(i2c)
oled = I2C_OLED(128, 64, i2c, folder)

gpio = {}
digital_output('furnace', board.D18)


data = DataBank(folder)
