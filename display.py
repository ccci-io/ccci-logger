#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont

from adafruit_ssd1306 import SSD1306_I2C

class I2C_OLED:

    def __init__(self, width, height, i2c, folder):
            
        disp = SSD1306_I2C(width, height, i2c)   # Pixel width and height.
        disp.fill(0)
        disp.show()
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, width, height), outline=0, fill=0)    # Clear image
        padding = -9
        self.top = padding
        self.bottom = height-padding
        self.x = 0   # Move left to right keeping track of the current x position for drawing shapes.
        self.image = image
        self.folder = folder
        self.width = width
        self.height = height
        self.lang = 'ru'
        self.disp = disp
        self.draw = draw
        self.vals = {
            'temperature': {
                'en': 'TEMPERATURE',
                'ru': 'ТЕМПЕРАТУРА',
            },
            'humidity': {
                'en': 'HUMIDITY',
                'ru': 'ВЛАЖНОСТЬ',
            }
        }

    def show_disp(self):
        self.disp.image(self.image)
        self.disp.show()

    def text(self, val):
        return self.vals[val][self.lang]

    def font(self, px):
        return ImageFont.truetype(self.folder + "res/Montserrat-Medium.ttf", px)

    def temperature(self, val):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.draw.text((self.x, self.top+8), self.text('temperature'), font=self.font(16), fill=255)
        self.draw.text((self.x, self.top+16), f"{round(val, 1)}°", font=self.font(50), fill=255)
        self.show_disp()

    def humidity(self, val):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.draw.text((self.x, self.top+8), self.text('humidity'), font=self.font(16), fill=255)
        self.draw.text((self.x, self.top+16), f"{round(val, 1)}%", font=self.font(50), fill=255)
        self.show_disp()

