#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import subprocess

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
        self.mode = 'large_humidity'
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
            self.draw.rectangle((125, 18, 128, 24), outline=0, fill=255)
        self.show_disp()


class OLED_Menu(I2C_OLED):

    def interface(self, mode=False, select=False):
        if mode:
            self.mode = mode
        if select:
            self.select = select
        getattr(self, self.mode)([self.select])
        #exec(f"self.{mode}([{select}])")
        
    def goto(self, button):
        self.interface(*self.controls[button])

    # # # ######### # LARGE DISPLAYS # ######### # # #

    def valid_select(self, select, items):
        if select >= len(items):
            select = 0
        return select


    def set_controls(self, menu):
        items = {
            'display_menu': [
                'large_temperature',
                'large_humidity',
                'stats',
                'network',
            ],
        }
        self.select = items[menu].index(self.mode)
        self.controls = {
            'up': [items[menu][self.valid_select(self.select-1, items[menu])]],
            'down': [items[menu][self.valid_select(self.select+1, items[menu])]],
            'left': [menu],
        }
    
    def large_display(self, var, val, unit):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.draw.text((self.x, self.top+8), self.text(var), font=self.font(16), fill=255)
        self.draw.text((self.x, self.top+16), f"{round(val, 1)}", font=self.font(50), fill=255)
        self.draw.text((self.x+100, self.top+24), f"{unit}", font=self.font(25), fill=255)
        self.show_disp()
        self.set_controls('display_menu')

    def large_temperature(self, ls=[0]):
        self.mode = 'large_temperature'
        self.large_display('temperature', self.data.sensors['temperature'], 'O')

    def large_humidity(self, ls=[0]):
        self.mode = 'large_humidity'
        self.large_display('humidity', self.data.sensors['humidity'], '%')

    def display_stats(self, *ls):
        draw = self.draw
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        height = 0
        for i in ls:
            draw.text((self.x, self.top+8+height), i[0], font=self.font(i[1]), fill=255)
            height += i[1]
        self.show_disp()

    def stats(self, ls=[0]):
        self.mode = 'stats'
        self.set_controls('display_menu')
        self.display_stats(
            ['STATS', 16],
            [f'TEMP:  {round(self.data.sensors["temperature"], 1)}°', 18],
            [f'HUMID: {round(self.data.sensors["humidity"], 1)}%', 18],
        )

    def network(self, ls=[0]):
        self.mode = 'network'
        self.set_controls('display_menu')
        # Shell scripts for system monitoring from here:
        # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "free -m | awk 'NR==2{printf \"%s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
        Ram = subprocess.check_output(cmd, shell=True).decode("utf-8")
        #cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%d GB  %s\", $3,$2,$5}'"
        #Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
        self.display_stats(
            ['NETWORK', 16],
            [f'IP: {IP}', 14],
            [f'CPU: {CPU}', 14],
            [f'RAM: {Ram}', 10],
        )
        #self.large('network', 12, '%')

    # # # ######### # MENUS # ######### # # #

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
