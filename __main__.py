#! /usr/bin/env python3

import asyncio
import sys
import os
#local
import controller


async def loop(func, args={}):
    while True:
        delay = getattr(controller, func)(**args)
        await asyncio.sleep(delay)

async def main():
    task = {}
    for i in controller.LOOPS:
        task[i[0]] = asyncio.create_task(loop(i[0]))
        
    for i in controller.LOOPS:    
        await task[i[0]]

async def input_enter():
    message = input("Press enter to quit\n\n")
    await message

### # TESTING # ###

def once(test=False):
    for i in controller.LOOPS:
        getattr(controller, i[0])(test=test, **i[1])

async def test():
    task = {}
    for i in controller.LOOPS:
        task[i[0]] = asyncio.create_task(loop(i[0], {'test': True, **i[1]}))
        
    for i in controller.LOOPS:    
        await task[i[0]]


if __name__ == "__main__":
    command = sys.argv[1]
    if command == 'once':
        once()
    elif command == 'testonce':
        once(True)
    elif command == 'only':
        getattr(controller, sys.argv[2])()
    elif command == 'test':
        asyncio.run(test())
    elif command == 'git':
        os.chdir(os.getcwd() + "//ccci-logger")
        os.system('git config --global user.name “ccci-io” \
            && git config --global user.email “i@ccci.io” \
                && git add . && git commit -m "Dev commits" \
                    && git push origin master')
    elif command == 'run':
        asyncio.run(main())
    #globals()['age']
