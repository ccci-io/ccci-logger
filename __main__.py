#! /usr/bin/env python3

import time
import asyncio
import json

#import board
#import busio

def beep(boop):
    if boop:
        return False
    else:
        return True

def read_settings():
    with open('/home/pi/ccci-controller/json/settings.json') as f:
        return json.load(f)

def write_settings(settings):
    with open('/home/pi/ccci-controller/json/settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

def log_data(data):
    with open('/home/pi/ccci-controller/log.json', 'a') as f:
        log = {
            'ts': int(time.time()),
            'sensors': data['sensors'],
            'flags': data['flags'],
        }
        json.dump(log, f)
        f.write(',\n')

def check(value, task, boo):
    alert = alerts[task]
    flag = flags[task]

    if boo:                             # If furnace is [off]
        arg = value < alert['on']       # TRUE if colder than [on] alert
    else:                               # If furnace is [on]
        arg = value > alert['off']      # TRUE if warmer than [off] alert

    if alert['on'] > alert['off']:      # Correction for air conditioning
        arg = beep(arg)

    if arg:
        if flag['check'] == boo:
            flag['on'] = boo
        else:
            flag['check'] = boo
    else:
        flag['check'] = beep(boo)

#async def print_after(flag, temp, delay):
#    print('30 SECOND DELAY STARTED')
#    await asyncio.sleep(delay)
#    print('Temp Check')

async def monitor(data, delay):
    boop = False
    while True:
        data['sensors'] = process.run(boop, folder)
        boop = beep(boop)
        await asyncio.sleep(delay)

async def operate(data, delay):
    while True:
        if data['flags']['furnace']['on']:
            check(data['sensors']['temp'], 'furnace', False)
        else:
            check(data['sensors']['temp'], 'furnace', True)
        log_data(data)
        await asyncio.sleep(delay)

async def main(data):
    a_monitor = asyncio.create_task(monitor(data, 1))
    a_operate = asyncio.create_task(operate(data, 30))
    await a_monitor
    await a_operate

if __name__ == "__main__":
    
    import thermostat as process

    folder = process.__file__[0:-11]

    data = {
        'alerts': read_settings(),
        'flags': {
            'furnace': {
                'check': False,
                'on': False,
            }
        },
        'sensors': {
            'temp': 0,
            'humidity': 0,
        },
    }

    data['sensors']['temp'] = data['alerts']['furnace']['off']

    asyncio.run(main(data))