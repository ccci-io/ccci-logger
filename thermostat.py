#!/usr/bin/env python3

import time
import board
import busio

from PIL import Image, ImageDraw, ImageFont

import adafruit_si7021
import adafruit_ssd1306

#print(adafruit_si7021.__file__)

class dotmap(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

i2c = busio.I2C(board.SCL, board.SDA)   # Create library object using Adafruit Bus I2C port
sensor = adafruit_si7021.SI7021(i2c)
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)   # Pixel width and height.

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)    # Get drawing object to draw on image.

draw.rectangle((0, 0, width, height), outline=0, fill=0)    # Clear image

padding = -9
top = padding
bottom = height-padding
x = 0   # Move left to right keeping track of the current x position for drawing shapes.

large_font = ImageFont.truetype("/home/pi/ccci-controller/res/Montserrat-Medium.ttf", 50)
small_font = ImageFont.truetype("/home/pi/ccci-controller/res/Montserrat-Medium.ttf", 16)

#with open('path_to_file/person.json') as f:
    #data = json.load(f)
print(__name__)

def heater_on():
    time.sleep(2)

def oled_temp(val):
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #draw.text((x, top+0), f"{sensor.temperature} C", font=font, fill=255)
    #draw.text((x, top+0), "%0.1f°" % val, font=font, fill=255)
    #draw.text((x, top+8), "TEMPERATURE", font=small_font, fill=255)
    draw.text((x, top+8), "ТЕМПЕРАТУРА", font=small_font, fill=255)
    #draw.text((x, top+8), "TEMP.", font=small_font, fill=255)
    draw.text((x, top+16), "%0.1f°" % val, font=large_font, fill=255)

def show_disp():
    disp.image(image)
    disp.show()

def beep_draw(boop):
    if boop:
        draw.rectangle((125, 0, 128, 3), outline=0, fill=100)

def run(boop, sets):
    oled_temp(sensor.temperature)
    beep_draw(boop)
    show_disp()
    
    #if sensor.temperature < low:
    #    flag_on(1)

    print("\nTemperature: %0.2f C" % sensor.temperature)
    print("Humidity: %0.1f %%" % sensor.relative_humidity)

    flags = {}

    #if sensor.temperature > low temp
    #flags['low_temp'] = False
    #flags['furnace_on'] = False
    #flags['high_temp'] = False
    

    output = {
        'temp': round(sensor.temperature, 2),
        'humidity': round(sensor.relative_humidity, 2),
    }

    return output
