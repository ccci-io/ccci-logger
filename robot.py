#!/usr/bin/env python3
import time
import sys
# pip install adafruit-blinka
import board
#local
from core.tasks import TaskBot
from core.circuitboard import CircuitBoard

# # # ############################### # # #
# # # #####      CLASS EXPANSION      # # #
# # # ############################### # # #



# # # ############################### # # #
# # # #####       LOOPS               # # #
# # # ############################### # # #

def main_loop(frequency=0):
    js = io.xbox() # js = joystick input
    if js:
        print(js)
        js_router(*js)
    time.sleep(frequency)
    #return frequency

# # # ############################### # # #
# # # #####       ROUTERS             # # #
# # # ############################### # # #

def js_router(key, value):
    #if key in ['touch_up', 'touch_down', 'touch_right', 'touch_left']:
    if key == 'lx_axis':
        io.servo(((value*(-1)+1)/2)*180)
    elif key == 'gas':
        io.m1a.value = True
        io.m1b.value = False
        io.gas((value+1)/2)

    elif key == 'brake':
        io.m1a.value = False
        io.m1b.value = True
        io.gas((value+1)/2)


folder = (__file__)[0:-13]

io = CircuitBoard()
io.xbox_input('xbox')
io.servo_output('servo', board.D23, duty_cycle=2 ** 15, frequency=50)

io.pwm_output('gas', board.D17, frequency=500)

io.digital_output('m1a', board.D27)
io.digital_output('m1b', board.D22)

if __name__ == "__main__":
    while True:
        main_loop()


# CIRCUIT CONSTRUCTORS & CONTROLLER INFERFACES
# CARBON COPY CONTROLLER INTERFACES
# COMPUTER CHIP CONTROLLER INTERFACES
# CONTROLLER CHIP & COMPUTER COMMON COMMUNICATE CONNECT CHANNEL COMMAND CHIEF CONDUCTOR