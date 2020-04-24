#!/usr/bin/env python3

import time
import board
import busio
#import sensors
#from sensors import I2C

from display import I2C_OLED

from PIL import Image, ImageDraw, ImageFont

from adafruit_si7021 import SI7021
from adafruit_ssd1306 import SSD1306_I2C

#print(adafruit_si7021.__file__)

class dotmap(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class MyDict(dict):
   def __getitem__(self, item):
       return dict.__getitem__(self, item) % self
#dictionary = MyDict({
#
#    'user' : 'gnucom',
#    'home' : '/home/%(user)s',
#    'bin' : '%(home)s/bin' 
#})

#vals = dotmap()


i2c = busio.I2C(board.SCL, board.SDA)   # Create library object using Adafruit Bus I2C port
sensor = SI7021(i2c)
oled = I2C_OLED(128, 64, i2c, '/home/pi/ccci-controller/')
disp = SSD1306_I2C(128, 64, i2c)   # Pixel width and height.

def sample(boop, sets):
    oled.temperature(sensor.temperature)

    print(f"\nTemperature: {round(sensor.temperature, 2)} C")
    print(f"Humidity: {round(sensor.relative_humidity, 2)} %")

    output = {
        'temp': round(sensor.temperature, 2),
        'humidity': round(sensor.relative_humidity, 2),
    }
    
    return output
