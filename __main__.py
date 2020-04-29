#! /usr/bin/env python3

import asyncio
import controller
import sys
import os



async def loop(func):
    while True:
        delay = getattr(controller, func)()
        await asyncio.sleep(delay)

async def main():
    await asyncio.gather(
        loop('respond'),
        loop('monitor'),
        loop('operate'),
    )

def test():
    controller.respond(test=True)
    controller.monitor(test=True)
    controller.operate(test=True)

if __name__ == "__main__":
    command = sys.argv[1]
    if command == 'test':
        test()
    elif command == 'git':
        os.chdir(os.getcwd() + "//ccci-controller")
        os.system('git config --global user.name “ccci-io” \
            && git config --global user.email “i@ccci.io” \
                && git add . && git commit -m "Dev commits" \
                    && git push origin master')
    else:
        asyncio.run(main())
    #globals()['age']

