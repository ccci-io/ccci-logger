#! /usr/bin/env python3

import asyncio
import sys
import os
#local
import controller

# LOOP CREATE FUNCTION
async def loop(func, args={}):
    while True:
        delay = getattr(controller, func)(**args)
        await asyncio.sleep(delay)

# MAIN ENGINE
async def main():
    task = {}
    for i in controller.LOOPS:
        #task[i[0]] = asyncio.create_task(loop(**i))
        task[i[0]] = asyncio.create_task(loop(i[0]))
        
    for i in controller.LOOPS:    
        await task[i[0]]

#async def input_enter():
#    message = input("Press enter to quit\n\n")
#    await message

### # TESTING # ###

async def test():
    task = {}
    for i in controller.LOOPS:
        task[i[0]] = asyncio.create_task(loop(i[0], {'test': True, **i[1]}))
        
    for i in controller.LOOPS:
        await task[i[0]]

def once(test=False):
    for i in controller.LOOPS:
        getattr(controller, i[0])(test=test, **i[1])



if __name__ == "__main__":
    command = sys.argv[1]
    if command == 'once':
        once()
    elif command == 'only':
        getattr(controller, sys.argv[2])()
    elif command == 'test':
        if len(sys.argv) > 2:
            if sys.argv[2] == once:
                once(True)
        else:
            asyncio.run(test())
    elif command == 'git':
        os.chdir(os.getcwd() + "//ccci-logger")
        os.system('git config --global user.name “ccci-io” \
            && git config --global user.email “i@ccci.io” \
                && git add . && git commit -m "Dev commits" \
                    && git push origin master')
    elif command == 'pull':
        os.chdir(os.getcwd() + "//ccci-logger")
        os.system('git config --global user.name “ccci-io” \
            && git config --global user.email “i@ccci.io” \
                && git pull https://github.com/ccci-io/ccci-logger.git')
    elif command == 'run':
        asyncio.run(main())
    else:
        asyncio.run(main())
    #globals()['age']
    
