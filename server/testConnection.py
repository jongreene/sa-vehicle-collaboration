import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART
import time

ble = Adafruit_BluefruitLE.get_provider()

data = ['{turn, left, 0, 0}', '{stop, all}', '{long-instruction-that-we-shouldn\'t-be-able-to-send, two_wheel, 50, 50}', '{stop, all}', '{turn, right, 0, 0}', '{stop, all}','{drive, four_wheel, 90, 0, 90, 0}', '{stop, all}']

def main():
    ble.clear_cached_data()
    adapter = ble.get_default_adapter()
    adapter.power_on()
    UART.disconnect_devices()

    try:
        adapter.start_scan()
        device = UART.find_device()
        if device is None:
            raise RuntimeError('Failed to find UART device!')
    finally:
        adapter.stop_scan()

    device.connect()

    try:
        UART.discover(device)
        uart = UART(device)

        global data
        global stop

        for d in data:
            safe_send(uart, d)

    finally:
        device.disconnect()


def send():
    ble.initialize()
    ble.run_mainloop_with(main)

def safe_send(uart, data):
    if data[-2:] != '\r\n':
        data = data + '\r\n'

    # if data is too long
    if len(data) > 16:
        # split it up
        data_substrings = list(chunkstring(data, 14))

        # and send each piece
        for string in data_substrings:
            safe_send(uart, string)

    # if data is short enough to fully send
    else:
        # send data
        uart.write(data.encode('UTF-8'))

        # while receiver nacks, retransmit
        while get_response(uart) != 'ack':
            uart.write(data.encode('UTF-8'))

def get_response(uart, timeout_sec=30):
    response = uart.read(timeout_sec)

    while response[-1] != '\n':
        response = response + uart.read(timeout_sec)

    return response.rstrip('\n').rstrip('\r')

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

send()
