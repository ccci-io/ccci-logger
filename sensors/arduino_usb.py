#!/usr/bin/python3

#sdi12_logger.py

import serial
import time


class SDI12:

    def __init__(self, port, bus='0'): #bytes("hello", encoding="ascii") 'hello'.encode('ascii')
        bus = bus.encode('ascii')
        self.cmd_sq = {
            'which' : [b'?!'],
            'id' : [bus+b'I!'],
            'verify' : [bus+b'V!'],
            'vwc': [bus+b'C0!', bus+b'D0!', bus+b'D1!'],
            'temp': [bus+b'C2!', bus+b'D0!', bus+b'D1!'],
            'volt': [bus+b'M9!', bus+b'D0!'],
        }   # https://www.fondriest.com/pdf/sentek_drill_drop_probe_manual.pdf
            # https://s.campbellsci.com/documents/ca/manuals/drill&drop_man.pdf
        # '/dev/ttyUSB0'
        self.ser = serial.Serial(
            port, # '/dev/ttyS0', '/dev/ttyUSB0'
            9600,
            timeout=2,
            write_timeout=2,
            )   # open serial port
                # print(self.ser.is_open)
                # self.ser.open()
        self.ser.flush()


    def cmd(self, command=b'?!', *options):
        #self.ser.send_break(duration=0.025)
        #time.sleep(.010)
        self.ser.write(command + b'\n')     # write a string
        
        ls = []
        if 'raw' in options:
            print(f'\n{command}:')
            print(self.ser.read(100))
        else:
            output = self.ser.read(100).decode('ASCII').split("+")
            
            #for i in range(0, len(output)):
            #    if i != 0:
            #        output[i] = float(output[i])
            #        ls.append(output[i])
                    
            for i in range(1, len(output)):
                output[i] = float(output[i])
                ls.append(output[i])
                    
        return ls

    def read(self, value, *options):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        ls = self.cmd_sq[value]
        output = []
        #print(f'\n{value}:')
        for i in ls:
            output.extend(self.cmd(i, *options))
        return output

    def test(self):
        for i in self.cmd_sq.keys():
            self.read(i, 'raw')

    def close(self):
        self.ser.close()

# FOR DIRECT TEST ONLY
if __name__ == "__main__":

    sensor = SDI12('/dev/serial0')
    #sensor.read('volt')
    sensor.read('temp', 'raw')
    sensor.cmd(b'?!')
    sensor.test()

    sensor.close()             # close port
