#!/usr/bin/env python3

import board
import busio
import digitalio

#local
from data import DataBank
from panel import SwitchBoard
from sensors.arduino_usb import SDI12
from tasks import TaskBot

from pprint import pprint
import time

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

class DATA(DataBank):
    def log(self, filepath, log, data):
        self.append(filepath, {
            'timestamp': int(time.time()),
            'log': log,
            'data': data,
        })

#ROUTER = {
#    'upload_data': {
#        'max_times': 5,
#        'postpone': tasks.time_from_now(minutes=5),
#        'condition': panel.io['modem'],
#    }
#}

#def respond(frequency=0.1, test=False):
#    status = panel.get_input()
#    if any(status.values()):
#        button = list(status.keys())[list(status.values()).index(True)]
#        #menu.goto(button)
#        #frequency = 0.5
#    return frequency

def usb():
    print(sdi12.get('vwc'))
    print(sdi12.get('temp'))

def log(frequency=3600, test=False):
    print('Log function called.')

    if not sdi12.ser.is_open:
        sdi12.ser.open()

    data.append('datalogger/log.json', {
            'timestamp': int(time.time()),
            'log': 'leduc-nslope-1-mc',
            'data': sdi12.get('vwc', 0),
        })
    
    log_filepath = 'datalogger/log.json'
    data.log(log_filepath, 'leduc-nslope-1-mc', sdi12.get('vwc', 0))
    data.log(log_filepath, 'leduc-nslope-1-temp', sdi12.get('temp', 0))

    data.append('datalogger/log.json', {
            'timestamp': int(time.time()),
            'log': 'leduc-nslope-1-temp',
            'data': sdi12.get('temp', 0),
        })
    
    if test:
        sdi12.test()
        print(sdi12.get('volt'))
        pprint(data)
    
    sdi12.ser.close()

    timeto = tasks.time_to_minute(5)
    if timeto < 59*60:
        frequency = timeto

    return frequency

def schedule(frequency=60, test=False):
    pprint(tasks.exe)
    pprint(tasks.ls)
    # Run all actions found in tasks.exe list as global() functions from here.
    if tasks.exe:
        for action in tasks.exe:
            #globals()[action]()
            router(action)
            del tasks.exe[action]

    return tasks.get_next()

#def router(action):
#    args = []
#    if '-' in action:
#        ls = action.split('-')
#        action, args = ls[0], ls[1:]
#    
#    if action in ROUTER:
#        ensure(action, *args, **ROUTER[action])
#    else:
#        globals()[action](*args)

# CARBON COPY CONTROLLER INDUSTRIES
# COPY CRAB CONTROLLER INDUSTRIES
# CHROME CRAB CONTROLLER INDUSTRIES
# CREATIVE CRAB CONTROLLER

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
    panel.io['modem'] = state
    
folder = (__file__)[0:-13]

data = DATA(folder)
tasks = TaskBot(TASKS)

#sdi12 = SDI12('/dev/ttyUSB0')  # SENTEK_USB
#sdi12 = SDI12('/dev/ttyACM0')   # ARDUINO 1200BAUD
#sdi12 = SDI12('/dev/ttyAMA0')   # ARDUINO 115200BAUD
sdi12 = SDI12('/dev/ttyACM0')   # ARDUINO 115200BAUD

panel = SwitchBoard()
panel.digital_output('modem', board.D18)
#panel.digital_input('button1', board.D17)

