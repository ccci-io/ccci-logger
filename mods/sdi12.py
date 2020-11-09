#!/usr/bin/python3

#sdi12_logger.py

import serial
import time


class SDI12:

    cmd_sq = {
        'id' : [b'I!'],
        'verify' : [b'V!'],
        'vwc': [b'C0!', b'D0!', b'D1!'],
        'temp': [b'C2!', b'D0!', b'D1!'],
        'volt': [b'M9!', b'D0!'],
    }   # https://www.fondriest.com/pdf/sentek_drill_drop_probe_manual.pdf
        # https://s.campbellsci.com/documents/ca/manuals/drill&drop_man.pdf
    # '/dev/ttyUSB0'
    
    def __init__(self, port):       #bytes("hello", encoding="ascii") 'hello'.encode('ascii') 'hello'.encode('utf-8')
        self.port = port
        #bus = bus.encode('ascii')

    def cmd(self, *arg, **kwarg):
        return self.cmd_write(*arg, **kwarg)
        
    def cmd_read(self, command=b'?!', raw=False):

        ls = []
        if raw:
            print(f'\n{command}:')
            print(self.ser.read(100))
        else:
            output = self.ser.read(100).decode('ascii').split("+")
            
            ### USE FOR SORTING VALUES (===)
            #for i in range(0, len(output)):
            #    if i != 0:
            #        output[i] = float(output[i])
            #        ls.append(output[i])
                    
            for i in range(1, len(output)):
                output[i] = float(output[i])
                ls.append(output[i])

        return ls

    def get(self, value, bus=0, raw=False):
        bus = str(bus).encode('ascii')
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        ls = self.cmd_sq[value]
        output = []
        for i in ls:
            output.extend(self.cmd(bus+i, *options))
        if raw:
            print(f'\n{value}:')
            print(output)
        return output
    
    def change_address(self, bus1, bus2):
        bus1, bus2 = str(bus1).encode('ascii'), str(bus2).encode('ascii')
        self.cmd(bus1 + b'A' + bus2 + b'!')

    def test(self, bus=0):
        for i in self.cmd_sq.keys():
            self.get(i, bus, 'raw')

    def close(self):
        self.ser.close()


class Arduino_USB(SDI12):
    ser = serial.Serial(
        self.port, # '/dev/ttyS0', '/dev/ttyUSB0'
        9600,
        timeout=2,
        write_timeout=2,
        )   # open serial port
            # print(self.ser.is_open)
            # self.ser.open()
    
    ser.flush()

    def cmd_write(self, *arg, **kwarg):
        self.ser.write(command + b'\n')     # write a string
        return self.cmd_read(*arg, **kwarg)


class Sentek_USB(SDI12):

    ser = serial.Serial(
        self.port, # '/dev/ttyS0', '/dev/ttyUSB0'
        1200,
        bytesize=serial.SEVENBITS,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        timeout=1.5,
        write_timeout=1.5,
        rtscts=False,
        dsrdtr=False,
        )   # open serial port
            # print(self.ser.is_open)
            # self.ser.open()

    ser.flush()

    def cmd_write(self, *arg, **kwarg):
        self.ser.send_break(duration=0.025)
        time.sleep(.010)
        self.ser.rts = True
        self.ser.write(command)     # write a string
        self.ser.rts = False
        time.sleep(.010)
        return self.cmd_read(*arg, **kwarg)


# FOR DIRECT TEST ONLY
if __name__ == "__main__":

    #sensor = Sentek_USB('/dev/ttyUSB0')    # USB SENTEK
    #sensor = Arduino_USB('/dev/ttyAMA0')     # USB ARDUINO???
    sensor = Arduino_USB('/dev/ttyACM0')     # USB ARDUINO
    sensor.get('volt')
    sensor.get('temp', 0, 'raw')
    sensor.cmd(b'?!')
    sensor.test()

    sensor.close()             # close port
