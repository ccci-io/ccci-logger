# Continuous Servo Test Program for CircuitPython
import time
import board
import pulseio
from adafruit_motor import servo
from analogio import AnalogIn

# create a PWMOut object on Pin A2.

#pwm = pulseio.PWMOut(board.A2, duty_cycle=0, frequency=50)
#pwm = pulseio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)
 
# Create a servo object, my_servo.
#my_servo = servo.ContinuousServo(pwm)

#############################
# CHANGE SERVO TO GET INPUT AND PUT POTENTIOMETER SEPARATELY
###############################

class Pot:
    def __init__(self, pin, const=65536):
        self.pin = analogio.AnalogIn(pin)
        self.const = const

    def reading(self, value=180):
        return (self.pin.value * value) / self.const

    def minmax(self, min_value=0, max_value=180):
        return ((self.pin.value * (max_value-min_value)) + min_value) / self.const

    def voltage(pin, value=3.3):
        return self.value(value)

# CircuitPython vs MicroPython

class Servo:
    servo_position = 90.0
    check = False

    def __init__(self, pin, frequency=50):
        pwm = pulseio.PWMOut(pin, frequency=frequency)
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
        servo1 = Servo(board.A2)
        pot = Pot(board.A7)
        servo1.instant_angle(pot.value(3.3))
        servo1.instant_angle(pot.value(180))
        time.sleep(0.1)