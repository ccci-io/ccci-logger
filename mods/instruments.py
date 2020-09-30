
#from mods.syslog import SYSLOG

#echo = SYSLOG(echo=True)

class Analog:
    def __init__(self, pin, const=65536):
        self.pin = pin
        self.const = const

    def value(self, value=180):
        return (self.pin.value * value) / self.const

    def minmax(self, min_value=0, max_value=180):
        return ((self.pin.value * (max_value-min_value)) + min_value) / self.const

    def voltage(self, volt=3.3):
        return self.value(volt)
    
    def __repr__(self, *args, **kwargs):
        return self.value(*args, **kwargs)

# CircuitPython vs MicroPython

class Servo:
    servo_position = 90.0
    check = False

    def __init__(self, servo):
        self.servo = servo
        #echo('Servo assigned ')
    
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
                #return f'Servo position: {input_angle}'
                #print('Servo position: ', input_angle)
