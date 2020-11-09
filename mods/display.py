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
    # # # ######### # MENU # ######### # # #
    
    lang_dict = [
        ['en', 'ru'],
        ['TEMPERATURE', 'ТЕМПЕРАТУРА'],
        ['HUMIDITY', 'ВЛАЖНОСТЬ'],
    ]
    mode = 'large_humidity'
    #mode = 'main_menu'
    select = 0
    boo = False
    controls = {}

    top = -9
    x = 0

    def __init__(self, disp, data):
        self.oled = I2C_OLED(disp)
        self.image = Image.new('1', (self.oled.width, self.oled.height))
        self.draw = ImageDraw.Draw(self.image)
        self.clear()
        self.data = data
        #self.bottom = disp.height-self.top

    def __call__(self, *args, **kwargs):
        return self.interface(*args, **kwargs)


    def interface(self, mode=False, select=False):
        if mode:
            self.mode = mode
        if select:
            self.select = select
        getattr(self, self.mode)(self.select)
        

    def translate(self, val):
        lang_index = self.lang_dict[0].index(self.data.lang)
        if lang_index:
            word_index = list(zip(*self.lang_dict))[0].index(val)
            return self.lang_dict[word_index][lang_index]

    # # # ############################### # # #
    # # # #####     IMAGE OPERATIONS      # # #
    # # # ############################### # # #

    def show(self):
        self.oled(self.image)
        
    def clear(self):
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)    # Clear image

    def font(self, px, select):
        if select == 'logo':
            filepath = "files/Montserrat-Medium.ttf"
        elif select == 'code':
            filepath = "files/Montserrat-Medium.ttf"
        else:
            filepath = "files/Montserrat-Medium.ttf"
        return ImageFont.truetype(self.data.folder + filepath, px)

    # # # ############################### # # #
    # # # #####      BUTTON CONTROLS      # # #
    # # # ############################### # # #

    def button_press(self, button):
        try:
            controls = self.controls[button]
            self.interface(*controls)
        except:
            pass

    def valid_select(self, select, items):
        if select >= len(items):
            select = 0
        return select

    def set_controls(self, menu_items, selected_menu):
        self.select = menu_items[selected_menu].index(self.mode)
        self.controls = {
            'up': [menu_items[selected_menu][self.valid_select(self.select-1, menu_items[selected_menu])]],
            'down': [menu_items[selected_menu][self.valid_select(self.select+1, menu_items[selected_menu])]],
            'left': [selected_menu],
        }

    # # # ############################### # # #
    # # # #####       LARGE DISPLAY       # # #
    # # # ############################### # # #
    
    def large_display(self, var, val, unit):
        self.clear()
        self.draw.text((self.x, self.top+8), self.translate(var), font=self.font(16), fill=255)
        self.draw.text((self.x, self.top+16), f"{round(val, 1)}", font=self.font(50), fill=255)
        self.draw.text((self.x+100, self.top+24), f"{unit}", font=self.font(25), fill=255)
        self.show()
        self.set_controls('display_menu')

    # # # ############################### # # #
    # # # #####     DISPLAY STATS         # # #
    # # # ############################### # # #

    def stats_display(self, *ls):
        self.clear()
        height = 0
        for i in ls:
            self.draw.text((self.x, self.top+8+height), i[0], font=self.font(i[1]), fill=255)
            height += i[1]
        self.show()

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
        self.stats_display(
            ['NETWORK', 16],
            [f'IP: {IP}', 14],
            [f'CPU: {CPU}', 14],
            [f'RAM: {Ram}', 10],
        )
        #self.large('network', 12, '%')

    # # # ############################### # # #
    # # # #####     SELECTABLE MENUS      # # #
    # # # ############################### # # #

    def menu_display(self, head, items, select):
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
        self.clear()
        draw = self.draw
        draw.text((self.x, self.top+8), head, font=self.font(16), fill=255)
        draw.text((self.x, self.top+24), top, font=self.font(12), fill=255)
        draw.text((self.x-2, self.top+34), center, font=self.font(20), fill=255)
        draw.text((self.x, self.top+56), bottom, font=self.font(12), fill=255)
        self.show()

    # # # ############################### # # #
    # # # #####     DEVELOPMENT TESTS     # # #
    # # # ############################### # # #

    def test(self):
        self.boo = not self.boo
        if self.boo:
            #self.draw.rectangle((125, 13, 128, 16), outline=0, fill=255)
            self.draw.rectangle((125, 8, 128, 17), outline=0, fill=255)
        else:
            #self.draw.rectangle((125, 17, 128, 20), outline=0, fill=255)
            self.draw.rectangle((125, 18, 128, 24), outline=0, fill=255)
        self.show()

