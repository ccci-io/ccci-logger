#! /usr/bin/env python3

import asyncio
import sys
import os
#local
import controller


async def loop(func, args=[]):
    while True:
        delay = getattr(controller, func)(**args)
        await asyncio.sleep(delay)

async def main():
    await asyncio.gather(
        loop('log'),
        loop('respond'),
        loop('schedule'),
    )

async def input_enter():
    message = input("Press enter to quit\n\n")
    await message

### # TESTING # ###

def once():
    controller.log(test=True)
    controller.respond(test=True)
    controller.schedule(test=True)

async def test():
    await asyncio.gather(
        loop('log', {'test': True, 'frequency': 60}),
        loop('respond', {'test': True}),
        loop('schedule', {'test': True}),
    )


if __name__ == "__main__":
    command = sys.argv[1]
    if command == 'once':
        once()
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
