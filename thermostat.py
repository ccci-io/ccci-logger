#!/usr/bin/env python3
from pprint import pprint
import time
import sys
# pip install adafruit-blinka
import board
#local
from core.data import DataBank
from core.tasks import TaskBot
from core.syslog import SYSLOG
from mods.circuitboard import CircuitBoard
from mods.display import OLED_Menu

# # # ############################### # # #
# # # #####      CLASS EXPANSION      # # #
# # # ############################### # # #

class DATA(DataBank):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings['temperature'] = 0
        self.settings['relative_humidity'] = 0

    def case_index(self, value):
        return super().indexOf(self.cases, 'name', value)

    def case_get(self, value):
        return self.cases[self.case_index(value)]

    def case_check(self, case_name, *args, **kwargs):
        case = self.case_get(case_name)
        self.flag_check(case, *args, **kwargs)

    def log_change(self, fresh, stable, log_name):
        change = self.custom_round(fresh, stable)
        if change:
            stable = change
            log(data=stable)


class MENU(OLED_Menu):

    # # # ############################### # # #
    # # # #####       LARGE DISPLAY       # # #
    # # # ############################### # # #
    
    def large_temperature(self, select):
        self.mode = 'large_temperature'
        self.large_display('TEMPERATURE', data.signal['temperature'], 'O')
        
    def large_humidity(self, select):
        self.mode = 'large_humidity'
        self.large_display('HUMIDITY', data.signal['relative_humidity'], '%')

    # # # ############################### # # #
    # # # #####     DISPLAY STATS         # # #
    # # # ############################### # # #

    def stats(self, select):
        self.mode = 'stats'
        self.set_controls('display_menu')
        self.stats_display(
            ['STATS', 16],
            [f'TEMP:  {round(data.signal["temperature"], 1)}°', 18],
            [f'HUMID: {round(data.signal["relative_humidity"], 1)}%', 18],
        )
    # # # ############################### # # #
    # # # #####     SELECTABLE MENUS      # # #
    # # # ############################### # # #

    def main_menu(self, select):
        self.mode = 'main_menu'
        items = [
            ['display_select', 'SELECT DISPLAY'],        # Display temp / humidity / stats
            ['heat_menu', 'SET HEAT'],          # Set alerts
            ['about', 'ABOUT'],                 # Version
        ]
        self.menu_display('MAIN MENU', items, select)

    def display_select(self, select):
        self.mode = 'display_menu'
        items = [       # 0 - FUNCTION .. 1 - DISPLAY TEXT
            ['large_temperature', 'TEMPERATURE'],
            ['large_humidity', 'HUMIDITY'],
            ['stats', 'STATISTICS'],
            ['network', 'NETWORK'],
        ]
        self.menu_display('DISPLAY MENU', items, select)

    # # # ############################### # # #
    # # # #####      BUTTON CONTROLS      # # #
    # # # ############################### # # #

    def set_controls(self, selected_menu)
        menu_items = {
            'display_menu': [
                'large_temperature',
                'large_humidity',
                'stats',
                'network',
            ],
        }
        return super().set_controls(menu_items, selected_menu)

# # # ############################### # # #
# # # #####       LOOPS               # # #
# # # ############################### # # #

def scan_input(frequency=0.5):
    pressed = io.scan_touch()
    if pressed:
        for signal in pressed:
            echo('Press detected on scan.')
            input_router(signal)
            #screen.button_press(signal)
            ######################### BUTTON ROUTER
            io.ghost_flag(signal)
            io.wake_up(signal)
    if io.wake:
        io.ghost_decay()
    
    time.sleep(frequency)
    #return frequency

def monitor(frequency=1):
    # Check for changes in temperature and humidity and log
    new_temperature = data.custom_round(io.sensor.temperature, data.temperature)
    new_humidity = data.custom_round(io.sensor.relative_humidity, data.relative_humidity)
 
    if new_temperature or new_humidity:
        new_data = {}
        if new_temperature:
            data.temperature = new_temperature
            new_data['tempc'] = data.temperature

        if new_humidity:
            data.relative_humidity = new_humidity
            new_data['humid'] = data.relative_humidity

        data.log(data=new_data)

    # Check if furnace needs to be turned on based on the active_case
    active_case = 'Default Furnace'
    case_check(active_case, io.furnace_out, data.temperature)

    # Refresh display
    display()

    # Execute scheduled tasks if in next 1 seconds
    if tasks.get_next(seconds=1):
        execute_tasks()

    # If wake status is True than scan this many times
    if io.wake:
        io.wake_check()
        scan_every = 0.2
    else:
        scan_every = 0.5

    for i in range(frequency/scan_every):
        scan_input(scan_every)


def execute_tasks():
    echo(tasks.exe)
    echo(tasks.ls)
    # Run all actions found in tasks.exe list as global() functions from here.
    for action in tasks.exe:
        #globals()[action]()
        action_router(action)
        del tasks.exe[action]


# PERIODIC LOG
def periodic_log(frequency=30):
    echo('Log function called.')

    data.log('files/thermostat_log.json', {'tempc': io.sensor.temperature, 'humid': io.sensor.relative_humidity}, )
    data.log('files/thermostat_log.json', {'humid': io.sensor.relative_humidity})

    timeto = tasks.time_to_minute(5)
    if timeto < 59*60:
        frequency = timeto

    return frequency

# # # ############################### # # #
# # # #####       ROUTERS             # # #
# # # ############################### # # #

def input_router(signal):
    if signal in ['touch_up', 'touch_down', 'touch_right', 'touch_left']:
        display.button_press(signal)
    elif signal in ['touch_run']:
        action_router(signal)


# ACTION ROUTER AND ENSURE
# Ensures that APIs are sent, if not log error and try again for <5 times> and if <modem_is_on>.
def action_router(action):
    args = []
    if '-' in action:
        ls = action.split('-')
        action, args = ls[0], ls[1:]
    
    if action in ENSURE:
        ensure(action, *args, **ENSURE[action])
    else:
        globals()[action](*args)

def ensure(action, postpone=False, max_times=5, condition=True, *args):
    print('Upload_data function called.')
    if not postpone:
        postpone = tasks.time_from_now(minutes=5)
    try:
        if condition and data.hang(action) < max_times:
            globals()[action](*args)
        data.reset_hanged(action)
    except:
        print(sys.exc_info()[0])
        data.log_error(tasks.iso_now(), sys.exc_info()[0])
        tasks.ls.append([postpone, action])
        tasks.sort_ls()

# # # ############################### # # #
# # # #####       ACTIONS             # # #
# # # ############################### # # #

def upload_data():
    'CREATE AN API'
    
def modem(state=True):
    print('Modem function called.')
    if state == 'off':
        state = False
    io.modem = state


def git_pull():
    print('Git_pull function called.')
    #os.chdir(os.getcwd() + "//crab-controller")
    #    os.system('git config --global user.name “ccci-io” \
    #        && git config --global user.email “i@ccci.io” \
    #            && git pull https://github.com/ccci-io/.git')



LOOPS = [ # [function, {test: params}]
    ['log', {'frequency': 10}],
    #['respond', {}],
    ['schedule', {}],
]

TASKS = [
    {   # Run pull request from git at <daily:12>
        'action': 'git_pull',   # Function
        #'second': 0,            # On <1-60>th second of minute. (DEFAULT=0)
        'minute': 10,            # On <1-60>th minute of hour. (DEFAULT=0)
        'hour': 12,             # On <1-24>th hour of day. <0> for every hour. (DEFAULT=0)
        #'day': 0,               # On <1-31>th day of month. <0> for every day. (DEFAULT=0)
        #'month': 0,             # On <1-12>th month of the year. <0> for every month. (DEFAULT=0)
        #'year': 0,              # On <2020+>th year. <0> for every year. (DEFAULT=0)
        #'isoweekday': 0,           # On <1-7> Monday. <0> for for every weekday. (DEFAULT=0)
    },
    {   # Turn on the modem on <daily:11-13>th hour of every day.
        'action': ['Day', 'Away', 'Day', 'Sleep'],    # a '-' separates action function (modem) and action args (modem(on), modem(off))
        'hour': [7, 9, 16, 21],
    },
]

ENSURE = {
    'upload_data': {
        'max_times': 5,
        'postpone': tasks.time_from_now(minutes=5),
        'condition': io.modem.value,
    }
}


echo = SYSLOG(True)
echo('THERMOSTAT is started.')


folder = (__file__)[0:-13]
data = DATA(folder)
data.load_settings('files/thermostat_settings.json')
data.set_log('files/thermostat_log.json')

io = CircuitBoard()
io.digital_input('touch_furnace', board.D18, scan=True)
io.digital_input('touch_up', board.D17, True)
io.digital_input('touch_down', board.D27, True)
io.digital_input('touch_left', board.D17, True)
io.digital_input('touch_right', board.D27, True)
io.digital_output('furnace_out', board.D17)
io.si72021('sensor')
io.ssd1306('oled', 128, 64)

display = MENU(io.oled, data)

tasks = TaskBot(data.TASKS)


# CARBON COPY CONTROLLER INDUSTRIES
# CARBON COPY CONTROLLER INTERFACES
# COPY CRAB CONTROLLER INDUSTRIES
# CHROME CRAB CONTROLLER INDUSTRIES
# CREATIVE CRAB CONTROLLER
# COMPUTER CHIP CONTROLLER INTERFACES
# CLOUD CENTRAL CONTROLLER INTERFACES
# CREATIVE CONTROLLERS
# COMPACT CONTROLLERS
# CONTROLLER CHIP & COMPUTER COMMON COMMUNICATE CONNECT CHANNEL COMMAND CHIEF
# INTERACT INTERGRATE INTERFACE INDUSTRIES 

js = {
    'Home': {
        'title': 'THIS IS WHAT IT IS',
        'cols': [
            ['TEMPERATURE:', '<v.1:temp>', 'DEG C'],
            ['HUMUDITY:', '$humid', '%'],
        ],
    }
}

