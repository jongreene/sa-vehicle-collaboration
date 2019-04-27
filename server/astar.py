import math
import random
import numpy as np
import time
from vehicle import Vehicle
import cv2 as cv
from queue import PriorityQueue

line_width = 1
line_color = (255, 0, 0)
file_name = 'path.png'
start_color = (0,255,0)
end_color = (0,0,255)
wall_color = (0,0,0)
open_color = (255,255,255)

class Node():
	"""A node class for A* Pathfinding"""

	def __init__(self, parent=None, position=None):
		self.parent = parent
		self.position = position

		self.g = 0
		self.h = 0
		self.f = 0

	def __eq__(self, other):
		return self.position == other.position

def n_closest(x,n,d=1):
    return x[n[0] - d:n[0] + d + 1, n[1] - d:n[1] + d + 1]

def is_wide_enough(maze, loc, next_loc, vehicle, scale):
	if scale > vehicle.width:
		return True

	thresh_grad = vehicle.clearance
	scale *= 1.4

	num_squares_width = math.ceil(vehicle.width / (2 * scale))
	num_squares_length = math.ceil(vehicle.length / (2 * scale))

	radius = max(num_squares_length, num_squares_width)

	if next_loc[0] - radius < 0 or next_loc[0] + radius >= len(maze) or next_loc[1] - radius < 0 or next_loc[1] + radius >= len(maze[0]):
		return False

	box = n_closest(maze, next_loc, radius)

	good = 0

	for i in box:
		for j in i:
			if abs(j - maze[next_loc[0]][next_loc[1]]) / scale > thresh_grad:
				break
			good += 1

	return good == len(box) * len(box[0])

def in_bounds(pos):
	global terrain
	(x, y) = pos
	return 0 <= x < len(terrain) and 0 <= y < len(terrain[0])

def passableFilter(terrain, pos, vehicle, scale):
	def f(next_pos):
		(x1, y1) = pos
		(x2, y2) = next_pos
		rise = terrain[x2][y2] - terrain[x1][y1]
		run = scale * get_cost(pos, next_pos)
		return vehicle.canTraverse(-np.arctan(rise / run), rise)
	return f

def wideFilter(vehicle, scale, maze):
	def w(pos):
		thresh_grad = vehicle.clearance
		s = scale * 1.4

		num_squares_width = math.ceil(vehicle.width / (2 * s))
		num_squares_length = math.ceil(vehicle.length / (2 * s))

		radius = max(num_squares_length, num_squares_width)

		if pos[0] - radius < 0 or pos[0] + radius >= len(maze) or pos[1] - radius < 0 or pos[1] + radius >= len(maze[0]):
			return False

		box = n_closest(maze, pos, radius)

		good = 0

		for i in box:
			for j in i:
				if abs(j - maze[pos[0]][pos[1]]) / s > thresh_grad:
					break
				good += 1

		return good == len(box) * len(box[0])
	return w


terrain = None

def neighbors(pos, terrain, vehicle, scale):
	(x, y) = pos
	results = [(x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1), (x+1, y), (x, y-1), (x-1, y), (x, y+1)]
	results = filter(in_bounds, results)
	pf = passableFilter(terrain, pos, vehicle, scale)
	results = filter(pf, results)
	wf = wideFilter(vehicle, scale, terrain)
	results = filter(wf, results)
	return results

def get_cost(c, n):
	return 1.4 if (c[0] - n[0]) * (c[1] - n[1]) else 1

def heuristic(a, b):
	(x1, y1) = a
	(x2, y2) = b
	return abs(x1 - x2) + abs(y1 - y2)

def findPath(maze, start, end, vehicle, unit, timeout=60):
	s_u = ''.join(i for i in unit if not i.isalpha())
	if not s_u: s_u = '1'
	clean_unit = float(s_u)
	global terrain
	terrain = maze
	frontier = PriorityQueue()
	frontier.put((0, start))
	came_from = {}
	cost_so_far = {}
	came_from[start] = None
	cost_so_far[start] = 0

	img = np.zeros((len(maze), len(maze[0]), 3), np.uint8)

	for i in range(len(maze)):
			for j in range(len(maze[0])):
				img[i][j] = wall_color if maze[i][j] == 0 else open_color

	while not frontier.empty():

		for x in frontier.queue:
			img[x[1][0]][x[1][1]] = line_color
		cv.imwrite(file_name, img)
		
		current = frontier.get()[1]

		if current == end:
			break

		for next in neighbors(current, maze, vehicle, clean_unit):
			new_cost = cost_so_far[current] + get_cost(current, next)
			if next not in cost_so_far or new_cost < cost_so_far[next]:
				cost_so_far[next] = new_cost
				priority = new_cost + heuristic(end, next)
				frontier.put((priority, next))
				came_from[next] = current

	current = end
	path = []
	while current != start:
		path.append(current)
		current = came_from[current]
	path.append(start)
	path.reverse()
	return path
	

# adapted from
# https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

# def findPath(maze, start, end, vehicle, unit, timeout=60):
# 	"""Returns a list of tuples as a path from the given start to the given end in the given maze"""

# 	s_u = ''.join(i for i in unit if not i.isalpha())
# 	if not s_u: s_u = '1'
# 	clean_unit = float(s_u)

# 	# Create start and end node
# 	start_node = Node(None, start)
# 	start_node.g = start_node.h = start_node.f = 0
# 	end_node = Node(None, end)
# 	end_node.g = end_node.h = end_node.f = 0

# 	# Initialize both open and closed list
# 	open_list = []
# 	closed_list = []

# 	# Add the start node
# 	open_list.append(start_node)

# 	start_time = time.time()

# 	# Loop until you find the end
# 	while len(open_list) > 0:

# 		# Get the current node
# 		current_node = open_list[0]
# 		current_index = 0
# 		for index, item in enumerate(open_list):
# 			if item.f < current_node.f:
# 				current_node = item
# 				current_index = index

# 		# Pop current off open list, add to closed list
# 		open_list.pop(current_index)
# 		closed_list.append(current_node)

# 		# Found the goal
# 		if current_node == end_node:
# 			path = []
# 			current = current_node
# 			while current is not None:
# 				path.append(current.position)
# 				current = current.parent
# 			return path[::-1] # Return reversed path

# 		# Generate children
# 		children = []
# 		for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

# 			# Get node position
# 			node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

# 			# Make sure within range
# 			if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
# 				continue

# 			rise = maze[node_position[0]][node_position[1]] - maze[current_node.position[0]][current_node.position[1]]
# 			run = clean_unit * 1.4 if new_position[0] != 0 and new_position[1] != 0 else clean_unit

# 			# Make sure walkable terrain (can we traverse)
# 			if not vehicle.canTraverse(-np.arctan(rise / run), rise):
# 				continue

# 			# Make sure terrain is wide enough to accomodate the vehicle
# 			if not is_wide_enough(maze, current_node.position, node_position, vehicle, clean_unit):
# 				continue
			
# 			# Create new node
# 			new_node = Node(current_node, node_position)

# 			# Append
# 			if new_node not in closed_list:
# 				children.append(new_node)

# 		# Loop through children
# 		for child in children:

# 			# Create the f, g, and h values
# 			child.g = current_node.g + 1
# 			child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
# 			child.f = child.g + child.h

# 			# Child is already in the open list
# 			in_open_list = False
# 			for open_node in open_list:
# 				if child == open_node and child.f > open_node.f:
# 					in_open_list = True

# 			if in_open_list:
# 				continue

# 			# Add the child to the open list
# 			open_list.append(child)

# 		if start_time + timeout < time.time():
# 			break

# 	img = np.zeros((len(maze), len(maze[0]), 3), np.uint8)

# 	for i in range(len(maze)):
# 		for j in range(len(maze[0])):
# 			img[i][j] = wall_color if maze[i][j] == 0 else open_color

# 	for i in range(len(closed_list)):
# 		temp = closed_list.pop()
# 		img[temp.position[0]][temp.position[1]] = line_color
# 	cv.imwrite(file_name, img)

# 	print("Image saved as '" + file_name + "'")