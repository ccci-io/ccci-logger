import time
# pip install adafruit-blinka
import board # https://github.com/adafruit/Adafruit_Blinka/blob/master/src/adafruit_blinka/board/raspberrypi/raspi_40pin.py
import busio
import digitalio
import analogio
import pulseio
# pip install adafruit-motor
from adafruit_motor import servo as adafruit_servo
# pip install adafruit-si7021
from adafruit_si7021 import SI7021
# pip install adafruit-ssd1306
from adafruit_ssd1306 import SSD1306_I2C
#local
from mods import instruments
from mods.syslog import SYSLOG

echo = SYSLOG(True)

class SwitchBoard:
    env = 'circuitpython'
    io = {}
    scan = {}
    outbound = {}
    wake = False

    i2c = False

    def __getattr__(self, key):
        return self.io[key]

    def __getitem__(self, key):
        return self.io[key]

    # Switch digital output
    def turn(self, signal, boo):
        self.io[signal].value = boo

    def scan_switch(self):
        pressed = []
        for signal in self.scan.keys():
            #arg = self.io[signal].value > 40
            if self.io[signal].value:
                pressed.append(signal)
        return pressed

    def scan_touch(self, true_value=40):
        pressed = []
        for signal in self.scan.keys():
            if self.io[signal].value > true_value:
                pressed.append(signal)
        return pressed

    def ghost_flag(self, signal, ghost=3):
        self.scan[signal] = ghost

    def ghost_decay(self):
        if sum(self.scan.values()):
            for value in self.scan.values():
                if value:
                    value -= 1

    def wake_up(self):
        self.wake = time.time()

    def wake_check(self):
        if time.time() - self.wake > 30:
            self.wake = False

    def scan_add(self, signal):
        self.scan[signal] = 0

    def __repr__(self):
        return self.io

class CircuitBoard(SwitchBoard):
    def __init__(self):
        echo('CircuitBoard initialized.')

    # Assign digital output
    def digital_output(self, signal, pin):
        self.io[signal] = digitalio.DigitalInOut(pin)
        self.io[signal].direction = digitalio.Direction.OUTPUT

    # Assign digital input
    def digital_input(self, signal, pin, scan=False):
        self.io[signal] = digitalio.DigitalInOut(pin)
        self.io[signal].direction = digitalio.Direction.INPUT
        self.io[signal].pull = digitalio.Pull.DOWN
        if scan:
            self.scan_add(signal)
        return self.io[signal]

    def analog_input(self, signal, pin, scan=False):
        self.io[signal] = instruments.Analog(analogio.AnalogIn(pin))
        if scan:
            self.scan_add(signal)
        return self.io[signal]

    def servo_output(self, signal, pin, *args, **kwargs):
        pwm = pulseio.PWMOut(pin, *args, **kwargs)
        self.io[signal] = instruments.Servo(adafruit_servo.Servo(pwm))
        return self.io[signal]

    def i2c_init(self):
        if not self.i2c:
            self.i2c = busio.I2C(board.SCL, board.SDA)
        return self.i2c

    def si7021(self, signal):
        i2c = self.i2c_init()
        self.io[signal] = SI7021(i2c)
        return self.io[signal]

    def ssd1306(self, signal, width, height)
        i2c = self.i2c_init()
        self.io[signal] = SSD1306_I2C(width, height)


if __name__ == "__main__":
    while True:
        io = CircuitBoard()
        io.analog_input('pot', board.A2)
        io.servo_output('servo', board.A6)

        io.servo.instant_angle(io.pot)

        time.sleep(0.1)