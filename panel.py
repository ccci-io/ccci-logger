import board # https://github.com/adafruit/Adafruit_Blinka/blob/master/src/adafruit_blinka/board/raspberrypi/raspi_40pin.py
import busio
import digitalio

class SwitchBoard:

    def __init__(self):
        self.io = {}
        self.button = 0
        self.digital_output('furnace', board.D18)
        self.digital_input('button1', board.D18)
        self.listen = [
            False,
            self.io['button1'].value,
        ]

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
        self.io[task].pull = digitalio.Pull.UP
    
    #def analog_input(self, task, pin):
    #    self.io[task] = analogio.AnalogIn(pin)
    
    def get_voltage(self, task):
        return (self.io[task].value * 3.3) / 65536

    def switch_true(self):
        if any(self.listen):
            self.button = self.listen.index(True)
