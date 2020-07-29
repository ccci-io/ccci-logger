#!/usr/bin/env python3

import board
import busio
import digitalio

#local
from bank import DataBank
from panel import SwitchBoard
from sentek_usb import SDI12
from check import TaskBot

LOOPS = [ # [function, {test: params}]
    ['log', {'frequency': 10}],
    #['respond', {}],
    ['schedule', {}],
]

TASKS = [
    {   # Run pull request from git at <daily:12>
        'task': 'git_pull', # Function
        'weekly': 0,        # On <1-7> Monday. <0> for all. (DEFAULT=0)
        'monthly': 0,       # On <1-31>th day of month. <0> for all. (DEFAULT=0)
        'daily': 12,        # On <1-24>th hour of day. <0> for hour. (DEFAULT=0)
        'hourly': 15,       # On <1-60>th minute of hour. (DEFAULT=0)
    },
    {   # Turn on the modem on <daily:11-13>th hour of every day.
        'task': ['modem_on', 'modem_off'],
        'daily': [11, 13],
    },
]

#def respond(frequency=0.1, test=False):
#    status = sb.get_input()
#    if any(status.values()):
#        button = list(status.keys())[list(status.values()).index(True)]
#        #menu.goto(button)
#        #frequency = 0.5
#    return frequency

def log(frequency=3600, test=False):
    print('Log function called.')

    if not sdi12.ser.is_open:
        sdi12.ser.open()

    sdi12.read('volt')
    sdi12.read('temp')
    sdi12.read('vwc')

    if test:
        sdi12.test()
    sdi12.ser.close()

    #data.sensors['temp'] = sdi12.read('temp')
    #data.sensors['mc'] = sdi12.read('vwc')
    #data.log()

    if test:
        print(data)
        #sdi12.cmd(b'0I!', 'raw')
        #sdi12.read('id', 'raw')


    return frequency

def schedule(frequency=60, test=False):
    return tasks.next()
    
folder = (__file__)[0:-13]

data = DataBank(folder)
tasks = TaskBot(TASKS)

sdi12 = SDI12('/dev/ttyUSB0')  # SENTEK_USB
#sdi12 = SDI12('/dev/ttyACM0')   # ARDUINO
#sdi12 = SDI12(/dev/ttyAMA0')   # TX/RX PINS?

sb = SwitchBoard()
sb.digital_output('modem', board.D18)
sb.digital_input('button1', board.D17)
sb.digital_input('button2', board.D27)
