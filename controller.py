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

LOOPS = [ # [function, {test: params}]
    ['log', {'frequency': 10}],
    #['usb', {}],
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
        'action': ['modem_on', 'modem_off'],
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

#def respond(frequency=0.1, test=False):
#    status = sb.get_input()
#    if any(status.values()):
#        button = list(status.keys())[list(status.values()).index(True)]
#        #menu.goto(button)
#        #frequency = 0.5
#    return frequency

def usb(frequency=3600, test=False):
    print('USB function called.')
    

    if not sdi12.ser.is_open:
        sdi12.ser.open()

    print(sdi12.read('temp'))
    print(sdi12.read('vwc'))
    print(sdi12.read('volt'))
    #sdi12.cmd(b'0D0!', 'raw')

    sdi12.ser.close()
    
    #print(sdi12.read('temp'))

def log(frequency=3600, test=False):
    print('Log function called.')

    if not sdi12.ser.is_open:
        sdi12.ser.open()

    data.sensors['mc'] = sdi12.read('vwc')
    data.sensors['temp'] = sdi12.read('temp')
    

    if test:
        sdi12.test()
        print(sdi12.read('volt'))
        print(data)
    
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
            globals()[action]()
            del tasks.exe[action]

    return tasks.get_next()


def git_pull():
    print('Git_pull function called.')
    #os.chdir(os.getcwd() + "//ccci-logger")
    #    os.system('git config --global user.name “ccci-io” \
    #        && git config --global user.email “i@ccci.io” \
    #            && git pull https://github.com/ccci-io/ccci-logger.git')

def upload_data():
    try:
        upload_data
    except:
        errors['upload_data']['time'] = sys.exc_info()[0]
        print(sys.exc_info()[0])
    print('Upload_data function called.')

def check_upload_data():
    print('Check_upload_data function called.')
    # Checks if data was uploaded today.
    upload_data()
    tasks.ls.append([tasks.time_from_now(minutes=5), 'check_upload_data'])
    tasks.sort_ls()

def modem_on():
    print('Modem_on function called.')
    sb.io['modem'] = True

def modem_off():
    print('Modem_off function called.')
    sb.io['modem'] = False
    
folder = (__file__)[0:-13]

data = DataBank(folder)
tasks = TaskBot(TASKS)

#sdi12 = SDI12('/dev/ttyUSB0')  # SENTEK_USB
#sdi12 = SDI12('/dev/ttyACM0')   # ARDUINO 1200BAUD
#sdi12 = SDI12('/dev/ttyAMA0')   # ARDUINO 115200BAUD
sdi12 = SDI12('/dev/ttyACM0')   # ARDUINO 115200BAUD

sb = SwitchBoard()
sb.digital_output('modem', board.D18)
#sb.digital_input('button1', board.D17)

