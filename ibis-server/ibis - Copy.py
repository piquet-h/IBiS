import asyncio
import struct
import sys
from bleak import BleakClient


address = "D6:D8:94:5E:21:03"

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

async def main(address):

    offset = 0

    def handle_disconnect(_: BleakClient):
        print("Device was disconnected, goodbye.")
        # cancelling all tasks effectively ends the program
        for task in asyncio.all_tasks():
            task.cancel()

    def handle_rx_bearing(sender, data):
        bearing = int.from_bytes(data, "little")
        print("bearing: {0}".format(bearing))
    
    def handle_rx_xyz(sender, data: bytearray):
        vector = struct.unpack("<hhh", data)
        print("xyz: {0}".format(vector))

    def handle_buttonA(sender, data):
        button = int.from_bytes(data, "little")
        print("ButtonA: {0}".format(button))

    def handle_buttonB(sender, data):
        button = int.from_bytes(data, "little")
        print("ButtonB: {0}".format(button))

    def handle_rx_uart(sender, data: bytearray):
        commandLine = data.decode('utf-8')
        tokens = commandLine.split(':')
        if(tokens[0] == 'OFFSET'):
            offset = tokens[1]
            print("New offset = {0}".format(offset))
        print("uart: {0}".format(commandLine))


    async with BleakClient(address, disconnect_callback=handle_disconnect) as client:
#        await client.start_notify(MAG_RX_BEARING_UUID, handle_rx_bearing)
#        await client.start_notify(MAG_RX_XYZ_UUID, handle_rx_xyz)
        await client.start_notify(UART_RX_CHAR_UUID, handle_rx_uart)
        await client.start_notify(BUTTON_RXA_UUID, handle_buttonA)
        await client.start_notify(BUTTON_RXB_UUID, handle_buttonB)

        loop = asyncio.get_running_loop()

        while True:
            data = await loop.run_in_executor(None, sys.stdin.buffer.readline)
            if not data:
                break

asyncio.run(main(address))