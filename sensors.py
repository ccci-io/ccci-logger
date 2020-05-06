#!/usr/bin/python3

#sdi12_logger.py

import serial
import time


class SDI12:

    def __init__(self, port):
        self.cmd_sq = {
            'which' : [b'?!'],
            'id' : [b'I!'],
            'verify' : [b'0V!', b'0D0!'],
            'mc': [b'0M1!', b'0D0!', b'0D1!', b'0D2!'],
            'mc1': [b'0M!', b'0D0!', b'0D1!', b'0D2!', b'0D3!', b'0D4!', b'0D5!', b'0D6!', b'0D7!', b'0D8!'],
            'mc2': [b'0MC!', b'0D0!', b'0D1!', b'0D2!'],
            'mc3': [b'0C!', b'0D0!', b'0D1!', b'0D2!'],
            'temp': [b'0M4!', b'0D0!', b'0D1!', b'0D2!'],
            'volt': [b'0M9!', b'0D0!']
        } # https://www.fondriest.com/pdf/sentek_drill_drop_probe_manual.pdf
        # '/dev/ttyUSB0'
        self.ser = serial.Serial(
            port, # '/dev/ttyS0', '/dev/ttyUSB0'
            1200,
            bytesize=serial.SEVENBITS,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
            write_timeout=1,
            rtscts=False,
            dsrdtr=False
            )  # open serial port
        #print(self.ser.is_open)
        #self.ser.open()

    def cmd(self, command=b'?!', options=[]):
        self.ser.send_break(duration=0.025)
        time.sleep(.010)
        self.ser.rts = True
        self.ser.write(command)     # write a string
        self.ser.rts = False
        ls = []
        if 'raw' in options:
            output = self.ser.read(100)
            print(output)
        else:
            output = self.ser.read(100).decode('ASCII').split('\r\n')[0].split("+")
            for i in range(0, len(output)):
                if i == 0:
                    output[i] = int(output[i])
                else:
                    output[i] = float(output[i])
                    ls.append(output[i])
        time.sleep(.010)
        return ls

    def read(self, value, options=['print']):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        ls = self.cmd_sq[value]
        output = []
        for i in ls:
            output.extend(self.cmd(i, options))
        if 'print' in options:
            print(output)
        return output

    def close(self):
        self.ser.close()

if __name__ == "__main__":

    sensor = SDI12()
    #sensor.read('volt')
    sensor.read('temp', ['raw'])
    #sensor.read('mc', ['raw'])
    sensor.read('mc', ['raw'])

    sensor.close()             # close port
