#!/usr/bin/env python3

import board
import busio
import digitalio

#local
from bank import DataBank
from panel import SwitchBoard
from sensors import SDI12

def logic_check(task):

    alert = data.alerts[task]
    flag = data.flags[task]
    value = data.sensors[alert['sensor']]

    boo = not flag['on']

    if boo:
        arg = value < alert['on']
    else:
        arg = value > alert['off']

    if alert['on'] > alert['off']:
        arg = not arg

    if arg:
        if flag['check'] == boo:
            flag['on'] = boo
            sb.turn(task, boo) #sb.io[task].value = boo
            
        else:
            flag['check'] = boo
    else:
        flag['check'] = not boo


def respond(frequency=0.1, test=False):
    status = sb.get_input()
    if any(status.values()):
        button = list(status.keys())[list(status.values()).index(True)]
        #menu.goto(button)
        #frequency = 0.5
    return frequency


def log(frequency=3600, test=False):

    if not sdi12.ser.is_open:
        sdi12.ser.open()

    #sdi12.read('volt')
    #sdi12.read('temp')
    #sdi12.read('vwc')
    #sdi12.cmd(b'0I!', 'raw')
    #sdi12.read('id', 'raw')
    if test:
        sdi12.test()
    sdi12.ser.close()

    #data.sensors['temp'] =
    #data.sensors['mc'] = 
    #data.log()

    if test:
        print(data)

    return frequency

def schedule(frequency=60, test=False):

    #schedule_check('modem')
    

    return frequency

folder = (__file__)[0:-13]

data = DataBank(folder)

#sdi12 = SDI12('/dev/ttyUSB0') #'/dev/ttyUSB0' for IO pins '/dev/ttyAMA0'
sdi12 = SDI12('/dev/ttyUSB0') #'/dev/ttyUSB0' for IO pins '/dev/ttyAMA0'

sb = SwitchBoard()
sb.digital_output('modem', board.D18)
sb.digital_input('button1', board.D17)
sb.digital_input('button2', board.D27)
