import subprocess
# pip install pillow
from PIL import Image, ImageDraw, ImageFont

#from adafruit_ssd1306 import SSD1306_I2C

class I2C_OLED:
    top = -9
    x = 0

    def __init__(self, disp):
        disp.fill(0)
        disp.show()
        self.disp = disp
        
    def __getattr__(self, key):
        return getattr(self.disp, key)

    def __call__(self, *args, **kwargs):
        return self.show_disp(*args, **kwargs)

    def show_disp(self, image):
        self.disp.fill(0) #################### yeah?
        self.disp.image(image)
        self.disp.show()
        
    #def large(self, var, val, unit):
    #    self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
    #    self.draw.text((self.x, self.top+8), self.text(var), font=self.font(16), fill=255)
    #    self.draw.text((self.x, self.top+16), f"{round(val, 1)}{unit}", font=self.font(50), fill=255)
    #    self.show_disp()

    #def show(self, val): # TESTING
    #    self.large('temperature', val, '°')


class OLED_Menu:
    
    lang = 'ru'
    lang_dict = [
        ['en', 'ru'],
        ['TEMPERATURE', 'ТЕМПЕРАТУРА'],
        ['HUMIDITY', 'ВЛАЖНОСТЬ'],
    ]

    # MENU
    mode = 'large_humidity'
    #mode = 'main_menu'
    select = 0
    boo = False
    controls = {}

    top = -9
    x = 0

    def __init__(self, disp, data):

        self.oled = I2C_OLED(disp)
        self.image = Image.new('1', (disp.width, disp.height))
        self.draw = ImageDraw.Draw(self.image)
        self.clear()
        
        self.folder = data.folder
        #self.bottom = disp.height-self.top

    def __call__(self, *args, **kwargs):
        return self.goto(*args, **kwargs)

    def interface(self, mode=False, select=False):
        if mode:
            self.mode = mode
        if select:
            self.select = select
        getattr(self, self.mode)(self.select)
        
    def goto(self, button):
        self.interface(*self.controls[button])

    def show(self):
        self.oled(self.image)

    # # # ######### # LARGE DISPLAYS # ######### # # #

    def text(self, val):
        lang_index = self.lang_dict[0].index(self.lang)
        if lang_index:
            word_index = list(zip(*self.lang_dict))[0].index(val)
            self.lang_dict[word_index][lang_index]

        return self.lang_dict[val][self.lang]

    def clear(self):
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)    # Clear image

    def font(self, px):
        return ImageFont.truetype(self.folder + "res/Montserrat-Medium.ttf", px)

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
        self.clear()
        self.draw.text((self.x, self.top+8), self.text(var), font=self.font(16), fill=255)
        self.draw.text((self.x, self.top+16), f"{round(val, 1)}", font=self.font(50), fill=255)
        self.draw.text((self.x+100, self.top+24), f"{unit}", font=self.font(25), fill=255)
        self.show()
        self.set_controls('display_menu')

    def show_temp(self, select):
        self.mode = 'large_temperature'
        

    def large_temperature(self, val):
        self.large_display('TEMPERATURE', val, 'O')

    def large_humidity(self, val):
        self.mode = 'large_humidity'
        self.large_display('HUMIDITY', val, '%')

    def display_stats(self, *ls):
        self.clear()
        height = 0
        for i in ls:
            self.draw.text((self.x, self.top+8+height), i[0], font=self.font(i[1]), fill=255)
            height += i[1]
        self.show()

    def stats(self, select):
        self.mode = 'stats'
        self.set_controls('display_menu')
        self.display_stats(
            ['STATS', 16],
            [f'TEMP:  {round(self.data.sensors["temperature"], 1)}°', 18],
            [f'HUMID: {round(self.data.sensors["humidity"], 1)}%', 18],
        )

    def network(self, select):
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
        self.show()

    def main_menu(self, select):
        self.mode = 'main_menu'
        select = ls[0]
        items = [
            ['display_menu', 'DISPLAY'],        # Display temp / humidity / stats
            ['heat_menu', 'SET HEAT'],          # Set alerts
            ['about', 'ABOUT'],                 # Version
        ]
        self.menu('MAIN MENU', items, select)

    def display_menu(self, select):
        self.mode = 'display_menu'
        select = ls[0]
        items = [       # 0 - FUNCTION .. 1 - DISPLAY TEXT
            ['large_temperature', 'TEMPERATURE'],
            ['large_humidity', 'HUMIDITY'],
            ['stats', 'STATISTICS'],
            ['network', 'NETWORK'],
        ]
        self.menu('DISPLAY MENU', items, select)

    def test(self):
        self.boo = not self.boo
        if self.boo:
            #self.draw.rectangle((125, 13, 128, 16), outline=0, fill=255)
            self.draw.rectangle((125, 8, 128, 17), outline=0, fill=255)
        else:
            #self.draw.rectangle((125, 17, 128, 20), outline=0, fill=255)
            self.draw.rectangle((125, 18, 128, 24), outline=0, fill=255)
        self.show()

