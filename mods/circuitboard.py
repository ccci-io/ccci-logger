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
#local
from core import instruments
from core.syslog import SYSLOG

echo = SYSLOG(True)


class CircuitBoard(instruments.SwitchBoard):
    def __init__(self):
        echo('CircuitBoard initialized.')

    # Assign digital output
    def digital_output(self, signal, pin, output=False):
        self.io[signal] = digitalio.DigitalInOut(pin)
        self.io[signal].direction = digitalio.Direction.OUTPUT
        self.io[signal].value = output

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

    def ssd1306(self, signal, width, height):
        i2c = self.i2c_init()
        self.io[signal] = SSD1306_I2C(width, height)


if __name__ == "__main__":
    while True:
        io = CircuitBoard()
        io.analog_input('pot', board.A2)
        io.servo_output('servo', board.A6)

        io.servo.instant_angle(io.pot)

        time.sleep(0.1)