import time

# pip install adafruit-blinka
import board # https://github.com/adafruit/Adafruit_Blinka/blob/master/src/adafruit_blinka/board/raspberrypi/raspi_40pin.py
import busio
import digitalio
import analogio
import pulseio

# pip install adafruit-motor
from adafruit_motor import servo as adafruit_servo
# pip install adafruit-si7021   # https://github.com/adafruit/Adafruit_CircuitPython_SI7021
from adafruit_si7021 import SI7021
# pip install adafruit-ssd1306
from adafruit_ssd1306 import SSD1306_I2C
import adafruit_lis3dh

#local
from core import instruments
#from core.xbox_js import Joystick

# SEPARATE CLASS FOR BUTTONS

class SwitchBoard:
    io = {}

    scan = False
    i2c = False
    spi = False

    # GET *.key
    def __getattr__(self, key):
        return self.io[key]

    # SET *.key = value
    def __setattr__(self, key, value):
        self.io[key] = value

    # GET *[key]
    def __getitem__(self, key):
        return self.io[key]

    # SET *[key] = value
    def __setitem__(self, key, value):
        self.io[key] = value

    # Get dictionary *.io
    def __repr__(self):
        return self.io

    def scan_switches(self, *args):
        if not self.scan:
            self.scan = instruments.ScanSwitch(*args)

    def duty_cycle(self, percent, duty_cycle=65535):
        return int(percent / 100.0 * float(duty_cycle))


class CircuitBoard(SwitchBoard):
    def __init__(self):
        print('CircuitBoard initialized.')

    # Switch digital output
    def turn(self, signal, boo):
        self.io[signal].value = boo

    # Assign digital output
    def digital_output(self, signal, pin):
        self.io[signal] = digitalio.DigitalInOut(pin)
        self.io[signal].direction = digitalio.Direction.OUTPUT
        self.io[signal].value = False

    # Assign digital input
    def digital_input(self, signal, pin):
        self.io[signal] = digitalio.DigitalInOut(pin)
        self.io[signal].direction = digitalio.Direction.INPUT
        self.io[signal].pull = digitalio.Pull.DOWN
        return self.io[signal]

    def analog_input(self, signal, pin):
        self.io[signal] = instruments.Analog(analogio.AnalogIn(pin))
        return self.io[signal]

    def servo_output(self, signal, pin, *args, **kwargs):
        pwm = pulseio.PWMOut(pin, *args, **kwargs)
        self.io[signal] = instruments.Servo(adafruit_servo.Servo(pwm))
        return self.io[signal]

    ### INITIALIZE PERIFERALS
    
    def i2c_init(self):
        if not self.i2c:
            self.i2c = busio.I2C(board.SCL, board.SDA)
        return self.i2c

    def si7021(self, signal):
        i2c = self.i2c_init()
        self.io[signal] = SI7021(i2c)
        return self.io[signal]

    def ssd1306(self, signal, width, height):
        i2c = self.i2c_init()
        self.io[signal] = SSD1306_I2C(width, height, i2c)

    def lis3dh(self, signal, int_pin):
        i2c = self.i2c_init()
        int1 = digitalio.DigitalInOut(int_pin)  # Set this to the correct pin for the interrupt!
        self.io[signal] = instruments.Accel(adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1))

    def xbox_input(self, signal):
        self.io[signal] = instruments.Joystick()


if __name__ == "__main__":
    while True:
        io = CircuitBoard()
        io.analog_input('pot', board.A2)
        io.servo_output('servo', board.A6)

        io.servo.instant_angle(io.pot)

        time.sleep(0.1)