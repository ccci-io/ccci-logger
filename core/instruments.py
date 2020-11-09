
from core.syslog import SYSLOG
import time

echo = SYSLOG(echo=True)

class ScanSwitch:
    switches = {}
    wake = False
    
    def __init__(self, io, *args):
        self.io = io
        self.scan_add(*args)

    def scan_switch(self, scan):
        pressed = []
        for signal in scan.keys():
            #arg = self.io[signal].value > 40
            if self.io[signal].value():
                pressed.append(signal)
        return scan, pressed

    def scan_touch(self, scan, trigger=200):
        pressed = []
        for signal in scan.keys():
            if self.io[signal].read() < trigger:
                pressed.append(signal)
        return scan, pressed

    def ghost_flag(self, signal, ghost=False):
        if ghost:
            self.switches[signal] = ghost
        else:
            try:
                return self.switches[signal]
            except:
                return 0

    def ghost_decay(self, scan):
        print(sum(scan.values()))
        if sum(scan.values()):
            for key, value in scan.items():
                if value:
                    scan[key] -= 1

    def detect_press(self, scan, pressed_d, wake):
        pressed = []
        if pressed_d:
            for signal in pressed_d:
                print('Press detected on scan.' + repr(pressed))
                pressed.append(signal)
                self.wake_up(wake)
                self.ghost_flag(signal, 2)
                
        if wake:
            self.ghost_decay(scan)
            self.wake_check(wake)
            
        return pressed, wake

    def wake_up(self, wake):
        wake = time.time()

    def wake_check(self, wake):
        if time.time() - wake > 30:
            wake = False

    def scan_add(self, *args):
        for signal in args:
            self.switches[signal] = 0


class Analog:
    def __init__(self, pin, duty_cycle=65536):
        self.pin = pin
        self.duty_cycle = duty_cycle

    def value(self, value=180):
        return (self.pin.value * value) / self.duty_cycle

    def minmax(self, min_value=0, max_value=180):
        return ((self.pin.value * (max_value-min_value)) + min_value) / self.duty_cycle

    def voltage(self, volt=3.3):
        return self.value(volt)
    
    def __repr__(self, *args, **kwargs):
        return self.value(*args, **kwargs)

class Accel:
    def __init__(self, signal):
        self.signal = signal
        #echo('Servo assigned ')

    def __call__(self):
        return self.raw()
    
    def raw(self):
        return self.signal.acceleration

    def angle(self):
        output = []
        inputs = self.g()
        for val in inputs:
            output.append(val * 90)
        return output

    def g(self):
        output = []
        for val in self.signal.acceleration:
            output.append(val / 9.806)
        return output

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


class PID:
    def __init__(self, P=0.2, I=0.0, D=0.0, current_time=None):
        echo('Initialized PID')

        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.sample_time = 0.00
        self.current_time = current_time if current_time is not None else time.time()
        self.last_time = self.current_time

        self.clear()

    def clear(self):
        # Clears PID computations and coefficients
        self.SetPoint = 0.0

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        # Windup Guard
        self.int_error = 0.0
        self.windup_guard = 20.0

        self.output = 0.0

    def update(self, feedback_value, current_time=None):
        """Calculates PID value for given reference feedback
        .. math::
            u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}
        .. figure:: images/pid_1.png
           :align:   center
           Test PID with Kp=1.2, Ki=1, Kd=0.001 (test_pid.py)
        """
        error = self.SetPoint - feedback_value

        self.current_time = current_time if current_time is not None else time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error

        if (delta_time >= self.sample_time):
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            # Remember last time and last error for next calculation
            self.last_time = self.current_time
            self.last_error = error

            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)

    def setKp(self, proportional_gain):
        # Determines how aggressively the PID reacts to the current error with setting Proportional Gain
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        # Determines how aggressively the PID reacts to the current error with setting Integral Gain
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        # Determines how aggressively the PID reacts to the current error with setting Derivative Gain
        self.Kd = derivative_gain

    def setWindup(self, windup):
        """Integral windup, also known as integrator windup or reset windup,
        refers to the situation in a PID feedback controller where
        a large change in setpoint occurs (say a positive change)
        and the integral terms accumulates a significant error
        during the rise (windup), thus overshooting and continuing
        to increase as this accumulated error is unwound
        (offset by errors in the other direction).
        The specific problem is the excess overshooting.
        """
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        # PID that should be updated at a regular interval.
        # Based on a pre-determined sampe time, the PID decides if it should compute or return immediately.
        self.sample_time = sample_time


class BLDC:
    def __init__(self):
        echo('Initialized Brushless DC')


def test_pid(P = 0.2,  I = 0.0, D= 0.0, L=100):
    """Self-test PID class
    .. note::
        ...
        for i in range(1, END):
            pid.update(feedback)
            output = pid.output
            if pid.SetPoint > 0:
                feedback += (output - (1/i))
            if i>9:
                pid.SetPoint = 1
            time.sleep(0.02)
        ---
    """
    pid = PID(P, I, D)

    pid.SetPoint=0.0
    pid.setSampleTime(0.01)



"""
class SwitchBoard:
    io = {}
    scan = {}
    outbound = {}
    wake = False
    i2c = False

    def __getattr__(self, key):
        return self.io[key]

    def __setattr__(self, key, value):
        self.io[key] = value

    def __getitem__(self, key):
        return self.io[key]

    def __setitem__(self, key, value):
        self.io[key] = value

    def __repr__(self):
        return self.io

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

    def scan_add(self, *args):
        for signal in args:
            self.scan[signal] = 0
        
    def duty_cycle(self, percent, duty_cycle=65535):
        return int(percent / 100.0 * float(duty_cycle))
"""