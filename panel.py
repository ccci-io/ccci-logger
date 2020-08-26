import board # https://github.com/adafruit/Adafruit_Blinka/blob/master/src/adafruit_blinka/board/raspberrypi/raspi_40pin.py
import busio
import digitalio

class SwitchBoard:

    def __init__(self):
        self.io = {}
        self.status = []

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
        self.io[task] = analogio.AnalogIn(pin)
    
    def get_voltage(self, task):
        return (self.io[task].value * 3.3) / 65536


class Schedule:

    def __init__(sch):      # (0) min, (13)th hour, (4)th day of the week
        ls = [60, 60, 24][0:len(sch)]
        self.secs = [a * b for a, b in zip(ls, sch)]

    def check():
        return


if __name__ == "__main__":
    sch = Schedule()