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
        #js_router(js)
    time.sleep(frequency)
    #return frequency

# # # ############################### # # #
# # # #####       ROUTERS             # # #
# # # ############################### # # #

def js_router(key, value):
    #if key in ['touch_up', 'touch_down', 'touch_right', 'touch_left']:
    if key == 'x':
        io.servo(value*180)
    elif key == 'y':
        pass


folder = (__file__)[0:-13]
io = CircuitBoard()
io.xbox_input('xbox')
io.servo_output('servo', board.A6)
#io.servo.instant_angle(io.pot)

if __name__ == "__main__":
    while True:
        main_loop()


# CARBON COPY CONTROLLER INTERFACES
# COMPUTER CHIP CONTROLLER INTERFACES
# CONTROLLER CHIP & COMPUTER COMMON COMMUNICATE CONNECT CHANNEL COMMAND CHIEF