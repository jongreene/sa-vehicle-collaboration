# https://github.com/adafruit/Adafruit_Python_BluefruitLE/blob/master/examples/uart_service.py

import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART
import time

debug = False

uart = None
data = None

ble = Adafruit_BluefruitLE.get_provider()

turn_values = {'90': .82, '-90': .84, '45': .42, '-45': .42}

data = [('90', '1'), ('90', '1'), ('90', '1'), ('90', '1')]

def turn(a):

	s = '{drive,two_wheel,'
	if int(a) > 0:
		s = s + '75,-75,'
	else:
		s = s + '-75,75,'

	s = s + str(turn_values[a]) + '}'

	send_cmd(s)

	return turn_values[a]

# d = distance in meters
def drive(d):
	# speed in meters per second when duty cycle = 75
	mps = 0.43406
	t = str(round((float(d) / mps), 4))
	s = '{drive,two_wheel,75,75,' + t + '}'
	send_cmd(s)
	return float(t)

def chunkstring(string, length):
	return (string[0+i:length+i] for i in range(0, len(string), length))

def send_cmd(string):
	global uart
	substrings = list(chunkstring(string + '\n', 16))
	debug and print('Substrings:', substrings)
	for s in substrings:
		uart.write(s.encode('UTF-8'))

	if 'hall' in string:
		while True:
			received = uart.read(timeout_sec=10)
			while received is not None and received[-1] != '\n':
				received = received + uart.read(timeout_sec=10)
			print(received[:-1])

	received = uart.read(timeout_sec=2)
	while received is not None and received[-1] != '\n':
		received = received + uart.read(timeout_sec=2)
	if received is not None:
		print('Received:', received[:-1])
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

		while debug:
			s = input('>> ')
			if s == 's':
				s = '{drive,two_wheel,0,0}'
				send_cmd(s)
			elif s.split(' ')[0] == 't':
				s1 = '{drive,two_wheel,' + s.split(' ')[1] + ',' + s.split(' ')[2] + '}'
				send_cmd(s1)
				time.sleep(float(s.split(' ')[3]))
				s = '{drive,two_wheel,0,0}'
				send_cmd(s)
			elif s.split(' ')[0] == 'd':
				move(s.split(' ')[1])
			elif s.split(' ')[0] == 'a':
				turn(s.split(' ')[1])
			elif len(s.split(' ')) == 2:
				s = '{drive,two_wheel,' + s.split(' ')[0] + ',' + s.split(' ')[1] + '}'
				send_cmd(s)
			elif len(s.split(' ')) == 3:
				s = '{drive,two_wheel,' + s.split(' ')[0] + ',' + s.split(' ')[1] + ',' + s.split(' ')[2] + '}'
				send_cmd(s)
			elif len(s.split(' ')) == 4:
				s = '{drive,four_wheel,' + s.split(' ')[0] + ',' + s.split(' ')[1] + ',' + s.split(' ')[2] + ',' + s.split(' ')[3] + '}'
				send_cmd(s)

			send_cmd(s)


		global data
		for d in data:
			time.sleep(turn(d[0] + 1))
			time.sleep(drive(d[1] + 1))

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
