from astar import *
from makeDirections import makeDirections
from connection import *
import numpy as np
from vehicle import Vehicle
import json
import os
import time

file_path = 'testTerrain.csv'
vehicle_file = 'vehicle.json'

terrain = np.genfromtxt(file_path, delimiter=',', dtype=float)

start = (15, 15)
end = (190, 190)

vehicle_opts = None
with open(vehicle_file, 'r') as j:
	vehicle_opts = json.load(j)
rover = Vehicle(vehicle_opts)
unit = '1cm'

# find a path through the terrain
print('Finding path... ', end='', flush=True)
path = findPath(terrain, start, end, rover, unit)
print('done')

# construct directions on how to follow path in desired format
print('Constructing vehicle instructions... ', end='')
directions = makeDirections(path, unit)
print('done')

# send directions to rover
print('Sending instructions to rover... ')
#send(directions)
