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
    with open(folder + 'settings.json') as f:
        return json.load(f)

def write_settings(settings):
    with open(folder + 'settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

def log_data(data, flags):
    with open(folder + 'log.json', 'a') as f:
        log = {
            'ts': int(time.time()),
            'data': data,
            'flags': flags,
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

async def monitor(info, delay):
    boop = False
    while True:
        info['data'] = process.run(boop, folder)
        boop = beep(boop)
        await asyncio.sleep(delay)

async def operate(info, delay):
    while True:
        if flags['furnace']['on']:
            check(info['data']['temp'], 'furnace', False)
        else:
            check(info['data']['temp'], 'furnace', True)
        log_data(info['data'], flags)
        await asyncio.sleep(delay)

async def main(info):
    a_monitor = asyncio.create_task(monitor(info, 1))
    a_operate = asyncio.create_task(operate(info, 30))
    await a_monitor
    await a_operate
    
if __name__ == "__main__":
    
    import thermostat as process

    folder = process.__file__[0:-11]

    alerts = read_settings()

    flags = {
        'furnace': {
            'check': False,
            'on': False,
        }
    }

    data = {
        'temp': alerts['furnace']['off'],
        'humidity': 0,
    }

    info = {
        'alerts': alerts,
        'flags': flags,
        'data': data,
    }

    asyncio.run(main(info))