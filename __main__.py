#! /usr/bin/env python3

import asyncio

async def monitor(delay):
    while True:
        controller.monitor()
        await asyncio.sleep(delay)

async def operate(delay):
    while True:
        controller.operate()
        await asyncio.sleep(delay)

async def main():
    a_monitor = asyncio.create_task(monitor(1))
    a_operate = asyncio.create_task(operate(30))
    await a_monitor
    await a_operate

if __name__ == "__main__":
    
    import controller
    asyncio.run(main())