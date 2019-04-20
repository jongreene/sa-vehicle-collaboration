# https://github.com/adafruit/Adafruit_Python_BluefruitLE/blob/master/examples/uart_service.py

import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART
import time

debug = True

uart = None
data = None

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

def main():
	ble.clear_cached_data()

	adapter = ble.get_default_adapter()
	adapter.power_on()
	debug and print('Using adapter: {0}'.format(adapter.name))

	debug and print('Disconnecting any connected UART devices...')
	UART.disconnect_devices()

	debug and print('Searching for UART device...')
	try:
		adapter.start_scan()
		device = UART.find_device()
		if device is None:
			raise RuntimeError('Failed to find UART device!')
	finally:
		adapter.stop_scan()

	debug and print('Connecting to device...')
	device.connect()

	try:
		debug and print('Discovering services...')
		UART.discover(device)

		global uart
		uart = UART(device)

		# global data
		# send data here

		while True:
			s = input('>> ')
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
		device.disconnect()


def send(incoming_data):
	global data
	data = incoming_data

	ble.initialize()
	ble.run_mainloop_with(main)


if __name__ == '__main__':
	ble.initialize()
	ble.run_mainloop_with(main)
