import asyncio
import time
import struct
import sys
import pynput

from bleak import BleakClient
from pynput.mouse import Button
from pynput.keyboard import Key

addressV1 = "E4:37:80:63:49:2B"
addressV2 = "D6:D8:94:5E:21:03"

mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()
offset = 0

UART_SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_RX_CHAR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

MAG_SERVICE__UUID = "e95df2d8-251d-470a-a062-fa1922dfa9a8"
MAG_RX_XYZ_UUID = 'e95dfb11-251d-470a-a062-fa1922dfa9a8'
MAG_RX_BEARING_UUID = 'e95d9715-251d-470a-a062-fa1922dfa9a8'
MAG_TX_PERIOD_UUID = 'e95d386c-251d-470a-a062-fa1922dfa9a8'
MAG_TX_1_UUID = 'e95db358-251d-470a-a062-fa1922dfa9a8'

BUTTON_SERVICE__UUID = 'e95d9882-251d-470a-a062-fa1922dfa9a8'
BUTTON_RXA_UUID = 'e95dda90-251d-470a-a062-fa1922dfa9a8'
BUTTON_RXB_UUID = 'e95dda91-251d-470a-a062-fa1922dfa9a8'


async def microbitV1():
    def handle_disconnect(_: BleakClient):
        print("Exiting V1")
        for task in asyncio.all_tasks():
            task.cancel()
        
    def handle_rx_uart(sender, data: bytearray):
        commandLine = data.decode('utf-8')
        print(commandLine)
        tokens = commandLine.split(':')
        if(tokens[0] == "SHAKE"):
            mouse.press(Button.right)
            mouse.release(Button.right)

    async with BleakClient(addressV1, disconnect_callback=handle_disconnect) as client:
        await client.start_notify(UART_RX_CHAR_UUID, handle_rx_uart)

        loop = asyncio.get_event_loop()
        while True:
            data = await loop.run_in_executor(None, sys.stdin.buffer.readline)
            if not data:
                break

async def microbitV2():

    def handle_disconnect(_: BleakClient):
        print("Exiting V2")
        # cancelling all tasks effectively ends the program
        for task in asyncio.all_tasks():
            task.cancel()

    def handle_rx_uart(sender, data: bytearray):
        commandLine = data.decode('utf-8')
        print(commandLine)
        tokens = commandLine.split(':')

        if(tokens[0] == "SHAKE"):
            mouse.press(Button.left)
            mouse.release(Button.left)
        elif(tokens[0] == "R"):
            mouse.move(int(tokens[2]), int(tokens[1]))


    def handle_buttonA(sender, data):
        button = int.from_bytes(data, "little")
        mouse.press(Button.left)
        mouse.release(Button.left)
        print("ButtonA: {0}".format(button))

    def handle_buttonB(sender, data):
        button = int.from_bytes(data, "little")
        mouse.press(Button.right)
        mouse.release(Button.right)
        print("ButtonB: {0}".format(button))

    async with BleakClient(addressV2, disconnect_callback=handle_disconnect) as client:
        await client.start_notify(UART_RX_CHAR_UUID, handle_rx_uart)
        await client.start_notify(BUTTON_RXA_UUID, handle_buttonA)
        await client.start_notify(BUTTON_RXB_UUID, handle_buttonB)

        loop = asyncio.get_event_loop()

        while True:
            data = await loop.run_in_executor(None, sys.stdin.buffer.readline)
            if not data:
                break   

async def main():
    await asyncio.gather(
        microbitV1(),
        microbitV2()        
    )

asyncio.run(main())