# Example of interaction with a BLE UART device using a UART service
# implementation.
# Author: Tony DiCola
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART
import time

uart = None
data = None

# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

def send_cmd(string):
    global uart
    substrings = list(chunkstring(string, 16))
    substrings.append('\n')
    for string in substrings:
        uart.write(string.encode('UTF-8'))
    received = uart.read(timeout_sec=60)
    while received[-1] != '\n':
        received = received + uart.read(timeout_sec=60)
    if received is not None:
        print(received[:-1])
    else:
        print('No data received')

# Main function implements the program logic so it can run in a background
# thread.  Most platforms require the main thread to handle GUI events and other
# asyncronous events like BLE actions.  All of the threading logic is taken care
# of automatically though and you just need to provide a main function that uses
# the BLE provider.
def main():
    # Clear any cached data because both bluez and CoreBluetooth have issues with
    # caching data and it going stale.
    ble.clear_cached_data()

    # Get the first available BLE network adapter and make sure it's powered on.
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))

    # Disconnect any currently connected UART devices.  Good for cleaning up and
    # starting from a fresh state.
    print('Disconnecting any connected UART devices...')
    UART.disconnect_devices()

    # Scan for UART devices.
    print('Searching for UART device...')
    try:
        adapter.start_scan()
        # Search for the first UART device found (will time out after 60 seconds
        # but you can specify an optional timeout_sec parameter to change it).
        device = UART.find_device()
        if device is None:
            raise RuntimeError('Failed to find UART device!')
    finally:
        # Make sure scanning is stopped before exiting.
        adapter.stop_scan()

    print('Connecting to device...')
    device.connect()  # Will time out after 60 seconds, specify timeout_sec parameter
                      # to change the timeout.

    # Once connected do everything else in a try/finally to make sure the device
    # is disconnected when done.
    try:
        # Wait for service discovery to complete for the UART service.  Will
        # time out after 60 seconds (specify timeout_sec parameter to override).
        print('Discovering services...')
        UART.discover(device)

        # Once service discovery is complete create an instance of the service
        # and start interacting with it.
        global uart
        uart = UART(device)

        # global data
        # SEND DATA HERE

        # Write a string to the TX characteristic.
        while True:
            s = input()
            if s == 's':
                s = '{drive,two_wheel,0,0}'
            elif len(s.split(' ')) == 2:
                s = '{drive,two_wheel,' + s.split(' ')[0] + ',' + s.split(' ')[1] + '}'
            elif len(s.split(' ')) == 4 and s.split(' ')[0] == 't':
                s1 = '{drive,two_wheel,' + s.split(' ')[1] + ',' + s.split(' ')[2] + '}'
                send(s1)
                time.sleep(float(s.split(' ')[3]))
                s = '{drive,two_wheel,0,0}'
            elif len(s.split(' ')) == 4:
                s = '{drive,four_wheel,' + s.split(' ')[0] + ',' + s.split(' ')[1] + ',' + s.split(' ')[2] + ',' + s.split(' ')[3] + '}'

            send_cmd(s)

    finally:
        # Make sure device is disconnected on exit.
        device.disconnect()


def send(incoming_data):
    global data
    data = incoming_data
    # Initialize the BLE system.  MUST be called before other BLE calls!
    ble.initialize()

    # Start the mainloop to process BLE events, and run the provided function in
    # a background thread.  When the provided main function stops running, returns
    # an integer status code, or throws an error the program will exit.
    ble.run_mainloop_with(main)


if __name__ == '__main__':
    ble.initialize()
    ble.run_mainloop_with(main)
