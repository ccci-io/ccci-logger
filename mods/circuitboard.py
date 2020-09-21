import board # https://github.com/adafruit/Adafruit_Blinka/blob/master/src/adafruit_blinka/board/raspberrypi/raspi_40pin.py
import busio
import digitalio
import analogio
import pulseio

from adafruit_motor import servo

import time


class MicroBoard:
    environment = 'micropython'

class CircuitBoard:
    environment = 'circuitpython'
    io = {}
    status = []
    #def __init__(self):

    # Switch digital output
    def turn(self, task, boo):
        self.io[task].value = boo

    # Assign digital output
    def digital_output(self, task, pin):
        self.io[task] = digitalio.DigitalInOut(pin)
        self.io[task].direction = digitalio.Direction.OUTPUT

    # Assign digital input
    def digital_input(self, task, pin):
        self.io[task] = digitalio.DigitalInOut(pin)
        self.io[task].direction = digitalio.Direction.INPUT
        self.io[task].pull = digitalio.Pull.DOWN
        self.status.append(task)

    def get_input(self):
        buttons = {}
        for task in self.status:
            buttons[task] = self.io[task].value
        return buttons
    
    def analog_input(self, task, pin):
        self.io[task] = Analog(analogio.AnalogIn(pin))
        self.out[task] = self.io[task].value()
        return self.io[task]

    def servo_output(self, task, pin, *args, **kwargs):
        pwm = pulseio.PWMOut(pin, *args, **kwargs)
        self.io[task] = servo.Servo(pwm)
        return self.io[task]

    def get_voltage(self, task):
        return (self.io[task].value * 3.3) / 65536

    def __repr__(self):
        return self.io


class Analog:
    def __init__(self, pin, const=65536):
        self.pin = pin
        self.const = const

    def value(self, value=180):
        return (self.pin.value * value) / self.const

    def minmax(self, min_value=0, max_value=180):
        return ((self.pin.value * (max_value-min_value)) + min_value) / self.const

    def voltage(self, volt=3.3):
        return (self.pin.value * volt) / self.const
    
    def __repr__(self, *args, **kwargs):
        return self.value(*args, **kwargs)

# CircuitPython vs MicroPython

class Servo:
    servo_position = 90.0
    check = False

    def __init__(self, pin, frequency=50, *args, **kwargs):
        pwm = pulseio.PWMOut(pin, frequency, *args, **kwargs)
        self.servo = servo.Servo(pwm)
    
    def instant_angle(self, input_angle):
        if abs(input_angle - self.servo_position) > 1:
            self.servo_position, self.servo.angle = [input_angle]*2
            print('Servo position: ', int(input_angle))

    def wait_angle(self, input_angle):
        if abs(input_angle - self.servo_position) > 1:
            self.check = True
            self.servo_position = input_angle
        else:
            if self.check:
                self.check = False
                self.servo.angle = input_angle
                print('Servo position: ', input_angle, ' @ ', time.now())
                #print('Servo position: ', input_angle)


if __name__ == "__main__":
    while True:
        io = CircuitBoard()
        io.analog_input('pot', board.A2)
        io.servo_output('servo', board.A6)

        io['servo'].instant_angle(io['pot'])
        io.servo.instant_angle(io.pot.value())


        servo1.instant_angle(pot.get_value())
        time.sleep(0.1)