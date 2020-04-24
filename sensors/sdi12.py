#!/usr/bin/python3

#sdi12_logger.py

import serial
import time

cmd_sq = {
    'which' : [b'?!'],
    'id' : [b'I!'],
    'mc': [b'0M!', b'0D0!', b'0D1!', b'0D2!'],
    'temp': [b'0M4!', b'0D0!', b'0D1!', b'0D2!'],
    'volt': [b'0M9!', b'0D0!']
}

# https://www.fondriest.com/pdf/sentek_drill_drop_probe_manual.pdf

ser = serial.Serial(
    '/dev/ttyUSB0',
    1200,
    bytesize=serial.SEVENBITS,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    timeout=1,
    write_timeout=1,
    rtscts=False,
    dsrdtr=False
    )  # open serial port
#print(ser.is_open)
#ser.open()


#def sdi12_raw(command=b'?!'):
#    ser.send_break(duration=0.025)
#    time.sleep(.010)
#    ser.rts = True
#    ser.write(command)     # write a string
#    ser.rts = False
#    #output = ser.read(100).replace('\r\n', '').split("+")
#    output = ser.read(100)
#    time.sleep(.010)
#    return output

def cmd(command=b'?!', options=[]):
    ser.send_break(duration=0.025)
    time.sleep(.010)
    ser.rts = True
    ser.write(command)     # write a string
    ser.rts = False
    ls = []
    if 'raw' in options:
        output = ser.read(100)
        print(output)
    else: 
        output = ser.read(100).decode('ASCII').split('\r\n')[0].split("+")
        for i in range(0, len(output)):
            if i == 0:
                output[i] = int(output[i]) 
            else:
                output[i] = float(output[i])
                ls.append(output[i])
    time.sleep(.010)
    return ls

def read(value, options=['print']):
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    ls = cmd_sq[value]
    output = []
    for i in ls:
        output.extend(cmd(i, options))
    if 'print' in options:
        print(output)
    return output

def close():
    ser.close()

if __name__ == "__main__":

    #read('volt')
    read('temp', ['raw'])
    #read('mc', ['raw'])
    read('mc', ['raw'])

    ser.close()             # close port
