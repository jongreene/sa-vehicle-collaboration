from astar import *
from makeDirections import makeDirections
#from connection import *
import numpy as np
from vehicle import Vehicle
import json
import os
import cv2 as cv

line_width = 1
line_color = (255, 0, 0)
file_name = 'path.png'
start_color = (0,255,0)
end_color = (0,0,255)
wall_color = (0,0,0)
open_color = (255,255,255)

file_path = 'testTerrain.csv'
vehicle_file = 'vehicle.json'

terrain = np.genfromtxt(file_path, delimiter=',', dtype=float)

# tell user if start and end points are invalid (too close to edge)
# or if end point is in radius, call that arrival
start = (10, 10)
#end = (len(terrain) - 1, len(terrain[0]) - 1)
end = (198, 198)

vehicle_opts = None
with open(vehicle_file, 'r') as j:
	vehicle_opts = json.load(j)
rover = Vehicle(vehicle_opts)
unit = '1cm'

# find a path through the terrain
print('Finding path... ', end='')
path = findPath(terrain, start, end, rover, unit)
print('done')

# construct directions on how to follow path in desired format
# print('Constructing vehicle instructions... ', end='')
# directions = makeDirections(path, unit)
# print('done')

# # send directions to rover
# print('Sending instructions to rover... ')
# send(directions)

img = np.zeros((len(terrain), len(terrain[0]), 3), np.uint8)

for i in range(len(terrain)):
	for j in range(len(terrain[0])):
		img[i][j] = wall_color if terrain[i][j] == 0 else open_color

for i in path:
	img[i[0]][i[1]] = line_color
cv.imwrite(file_name, img)

print("Image saved as '" + file_name + "'")
