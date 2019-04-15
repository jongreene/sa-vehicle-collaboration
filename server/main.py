from astar import *
from makeDirections import makeDirections
from connection import *
import numpy as np
from vehicle import Vehicle
import json
import os

file_path = 'terrain.csv'
vehicle_file = 'vehicle.json'

terrain = np.genfromtxt(file_path, delimiter=',')
start = (0, 0)
end = (len(terrain) - 1, len(terrain[0]) - 1)

vehicle_opts = None
with open(vehicle_file, 'r') as j:
	vehicle_opts = json.load(j)
rover = Vehicle(vehicle_opts)
unit = '15cm'

# find a path through the terrain
print('Finding path... ', end='')
path = findPath(terrain, start, end, rover, unit)
print('done')

# construct directions on how to follow path in desired format
print('Constructing vehicle instructions... ', end='')
directions = makeDirections(path, unit)
print('done')

# send directions to rover
print('Sending instructions to rover... ')
send(directions)
