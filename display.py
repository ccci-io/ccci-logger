#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont

from adafruit_ssd1306 import SSD1306_I2C

class I2C_OLED:

    def __init__(self, width, height, i2c, folder, data):
            
        disp = SSD1306_I2C(width, height, i2c)   # Pixel width and height.
        disp.fill(0)
        disp.show()
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, width, height), outline=0, fill=0)    # Clear image
        padding = -9
        self.data = data
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

        # MENU
        self.mode = 'large_temperature'
        #self.mode = 'main_menu'
        self.select = 0
        self.boo = False
        self.controls = {}

    def show_disp(self):
        self.disp.image(self.image)
        self.disp.show()

    def text(self, val):
        return self.vals[val][self.lang]

    def font(self, px):
        return ImageFont.truetype(self.folder + "res/Montserrat-Medium.ttf", px)

    def large(self, var, val, unit):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.draw.text((self.x, self.top+8), self.text(var), font=self.font(16), fill=255)
        self.draw.text((self.x, self.top+16), f"{round(val, 1)}{unit}", font=self.font(50), fill=255)
        self.test()
        self.show_disp()
        


    def show(self): # TESTING
        self.large('temperature', self.data.sensors['temperature'], '°')

    def test(self):
        self.boo = not self.boo
        if self.boo:
            #self.draw.rectangle((125, 13, 128, 16), outline=0, fill=255)
            self.draw.rectangle((125, 8, 128, 17), outline=0, fill=255)
        else:
            #self.draw.rectangle((125, 17, 128, 20), outline=0, fill=255)
            self.draw.rectangle((125, 17, 128, 24), outline=0, fill=255)


class OLED_Menu(I2C_OLED):

    # # # ######### # DISPLAYS # ######### # # #
    
    def interface(self, mode=False, select=0):
        if mode:
            self.mode = mode
        getattr(self, self.mode)([select])
        
        #exec(f"self.{mode}([{select}])")
        
    def goto(self, button):
        self.interface(*self.controls[button])

    def large_temperature(self, ls=[0]):
        self.mode = 'large_temperature'
        self.controls['left'] = ['display_menu']
        #self.controls = {
        #    'up': 'network',
        #    'down': 'large_humidity',
        #    'left': 'display_menu',
        #}
        self.large('temperature', self.data.sensors['temperature'], '°')
        # FIND INDEX OF display_menu and set that as self.select

    def large_humidity(self):
        self.mode = 'large_humidity'
        self.controls = {
            'up': ['large_temperature'],
            'down': ['network'],
            'left': ['display_menu'],
        }
        self.large('humidity', self.data.sensors['humidity'], '%')

    def network(self):
        self.mode = 'network'
        self.controls = {
            'up': ['large_temperature'],
            'down': ['network'],
            'left': ['display_menu'],
        }
        #self.large('network', 12, '%')

    def menu(self, head, items, select):
        # Loop select number if goes above the amount in the list
        if abs(select) == len(items):
            select = 0
        self.select = select
        self.controls = {
            'up': [self.mode, select-1],
            'down': [self.mode, select+1],
            'right': [items[select][0], 0],
        }
        top, center, bottom = items[select-1][1], items[select][1], items[select+1][1]
        draw = self.draw
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        draw.text((self.x, self.top+8), head, font=self.font(16), fill=255)
        draw.text((self.x, self.top+24), top, font=self.font(12), fill=255)
        draw.text((self.x-2, self.top+34), center, font=self.font(20), fill=255)
        draw.text((self.x, self.top+56), bottom, font=self.font(12), fill=255)

        self.show_disp()

    def main_menu(self, ls=[0]):
        self.mode = 'main_menu'
        select = ls[0]
        items = [
            ['display_menu', 'DISPLAY'],        # Display temp / humidity / stats
            ['heat_menu', 'SET HEAT'],          # Set alerts
            ['about', 'ABOUT'],                 # Version
        ]
        self.menu('MAIN MENU', items, select)


    def display_menu(self, ls=[0]):
        self.mode = 'display_menu'
        select = ls[0]
        items = [       # 0 - FUNCTION .. 1 - DISPLAY TEXT
            ['large_temperature', 'TEMPERATURE'],
            ['large_humidity', 'HUMIDITY'],
            ['stats', 'STATISTICS'],
            ['network', 'NETWORK'],
        ]
        self.menu('DISPLAY MENU', items, select)
