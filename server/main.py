from astar import *
from makeDirections import makeDirections
import numpy as np
from vehicle import Vehicle
import json
import os
import time

running_on_pi = False

file_path = 'room_scan.csv'
vehicle_file = 'vehicle.json'

terrain = np.genfromtxt(file_path, delimiter=',', dtype=float)
start = (11,3)
end = (28, 40)

vehicle_opts = None
with open(vehicle_file, 'r') as j:
	vehicle_opts = json.load(j)
rover = Vehicle(vehicle_opts)
unit = '30.5cm'

# find a path through the terrain
print('Finding path... ', end='', flush=True)
path = findPath(terrain, start, end, rover, unit)
print('done')

# construct directions on how to follow path in desired format
print('Constructing vehicle instructions... ', end='')
directions = makeDirections(path, unit)
print('done')

# send directions to rover
if running_on_pi:
	from connection import *
	print('Sending instructions to rover... ')
	send(directions)

if not running_on_pi:
	import cv2 as cv

	line_width = 1
	line_color = (255, 0, 0)
	file_name = 'path.png'
	start_color = (0,255,0)
	end_color = (0,0,255)
	wall_color = (0,0,0)
	open_color = (255,255,255)

	img = np.zeros((len(terrain), len(terrain[0]), 3), np.uint8)

	for i in range(len(terrain)):
		for j in range(len(terrain[0])):
			img[i][j] = wall_color if terrain[i][j] != 0 else open_color

	for i in path:
		img[i[0]][i[1]] = line_color
	cv.imwrite(file_name, img)

	print("Image saved as '" + file_name + "'")
