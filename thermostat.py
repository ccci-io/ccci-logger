#!/usr/bin/env python3
from pprint import pprint
import time
import sys
# pip install adafruit-blinka
import board
#local
from mods.data import DataBank
from mods.circuitboard import CircuitBoard
from mods.tasks import TaskBot
from mods.syslog import SYSLOG


class DATA(DataBank):
    def log(self, filepath, data):
        self.append(filepath, {
            'timestamp': int(time.time()),
            'data': data,
        })


def input_router(signal):
    if signal in ['touch_up', 'touch_down', 'touch_right', 'touch_left']:
        menu.goto(signal)
    elif signal in ['touch_run']:
        action_router(signal)


def scan_input(frequency=0.5, test=False):
    pressed = io.scan_touch()
    if pressed:
        for signal in pressed:
            input_router(signal)
            #menu.goto(signal)
            ######################### BUTTON ROUTER
            io.ghost_flag(signal)
            io.wake_up(signal)
    if io.wake:
        io.ghost_decay()
        frequency = 0.2

    return frequency


def display(frequency=1):
    if io.wake:
        io.wake_check()

# DYNAMIC LOG
def log_change(frequency=30):
    echo('Log change')

# PERIODIC LOG
def log(frequency=30):
    echo('Log function called.')
    data.log('files/thermostat_log.json', io.sensor)

    timeto = tasks.time_to_minute(5)
    if timeto < 59*60:
        frequency = timeto

    return frequency

def schedule(frequency=60):
    pprint(tasks.exe)
    pprint(tasks.ls)
    # Run all actions found in tasks.exe list as global() functions from here.
    if tasks.exe:
        for action in tasks.exe:
            #globals()[action]()
            action_router(action)
            del tasks.exe[action]

    return tasks.get_next()


def action_router(action):
    args = []
    if '-' in action:
        ls = action.split('-')
        action, args = ls[0], ls[1:]
    
    if action in ROUTER:
        ensure(action, *args, **ROUTER[action])
    else:
        globals()[action](*args)


def git_pull():
    print('Git_pull function called.')
    #os.chdir(os.getcwd() + "//crab-controller")
    #    os.system('git config --global user.name “ccci-io” \
    #        && git config --global user.email “i@ccci.io” \
    #            && git pull https://github.com/ccci-io/.git')

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

def upload_data():
    'CREATE AN API'
    
def modem(state=True):
    print('Modem function called.')
    if state == 'off':
        state = False
    io.modem = state



js = {
    'Home': {
        'title': 'THIS IS WHAT IT IS',
        'cols': [
            ['TEMPERATURE:', '<v.1:temp>', 'DEG C'],
            ['HUMUDITY:', '$humid', '%'],
        ],
    }
}


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
            io.turn(task, boo) #io.io[task].value = boo
            
        else:
            flag['check'] = boo
    else:
        flag['check'] = not boo


def monitor(frequency=1, test=False):

    data.sensors['temperature'] = round(sensor.temperature, 1)
    data.sensors['humidity'] = round(sensor.relative_humidity, 1)

    menu.interface()

    if test:
        menu.test()
        print(f"\nTemperature: {round(sensor.temperature, 2)} C")
        print(f"Humidity: {round(sensor.relative_humidity, 2)} %")
        print(data)

    return frequency


def operate(frequency=30, test=False):

    check('furnace')
    data.log()

    return frequency


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
        'action': ['modem-on', 'modem-off'],    # a '-' separates action function (modem) and action args (modem(on), modem(off))
        'hour': [11, 13],
    },
    {
        'action': 'upload_data',
        'hour': 11,
        'minute': 10,
    },
    {
        'action': 'check_upload_data',
        'hour': 11,
        'minute': 20,
    },
]

ROUTER = {
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

io = CircuitBoard()
io.digital_input('touch_furnace', board.D18, scan=True)
io.digital_input('touch_up', board.D17, True)
io.digital_input('touch_down', board.D27, True)
io.digital_input('touch_left', board.D17, True)
io.digital_input('touch_right', board.D27, True)
io.digital_output('furnace_out', board.D17)
io.si72021('sensor')
io.ssd1306('oled', 128, 64)

menu = OLED_Menu(io.oled, data)

tasks = TaskBot(data.TASKS)


# CARBON COPY CONTROLLER INDUSTRIES
# COPY CRAB CONTROLLER INDUSTRIES
# CHROME CRAB CONTROLLER INDUSTRIES
# CREATIVE CRAB CONTROLLER
# COMPUTER CHIP CONTROLLER INTERFACES
# CLOUD CENTRAL CONTROLLER INTERFACES
# CREATIVE CONTROLLERS