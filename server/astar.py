import math
import random
import numpy as np
import time
from vehicle import Vehicle

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

def is_wide_enough(maze, loc, next_loc, vehicle, scale):
	thresh_grad = vehicle.clearance

	#Determine which direction were going
	heading = 0
	#going up or down
	if loc[0] != next_loc[0] and loc[1] == next_loc[1]:
		heading = 90

	# going left or right
	elif loc[0] == next_loc[0] and loc[1] != next_loc[1]:
		heading = 0

	# going NE or SW
	elif next_loc[0] * next_loc[1] > 0:
		heading = 45

	# going NW or SE
	elif next_loc[0] * next_loc[1] < 0:
		heading = 135

	# if going at 45, 135, etc change scale
	if heading != 0 or heading != 90:
		scale *= 1.4

	if scale > vehicle.width:
		return True

	num_squares = math.ceil(vehicle.width / scale)
	check_1 = []
	check_2 = []

	if heading == 90:
		for n in range(num_squares):
			check_1.append(maze[loc[0]][loc[1] + n + 1])
		for n in range(num_squares):
			check_2.append(maze[loc[0]][loc[1] - n - 1])

	elif heading == 0:
		for n in range(num_squares):
			check_1.append(maze[loc[0] + n + 1][loc[1]])
		for n in range(num_squares):
			check_2.append(maze[loc[0] - n - 1][loc[1]])

	elif heading == 45:
		for n in range(num_squares):
			check_1.append(maze[loc[0] - n - 1][loc[1] + n + 1])
		for n in range(num_squares):
			check_2.append(maze[loc[0] + n + 1][loc[1] - n - 1])

	else:
		for n in range(num_squares):
			check_1.append(maze[loc[0] + n + 1][loc[1] + n + 1])
		for n in range(num_squares):
			check_2.append(maze[loc[0] - n - 1][loc[1] - n - 1])

	good = 0
	now_pos = maze[loc[0]][loc[1]]
	# TODO: run through each of the can node and see if it can traverse then increment good if so
	for pos in check_1:
		if abs(pos - now_pos)/scale > thresh_grad:
			break
		good += 1
		now_pos = pos

	now_pos = maze[loc[0]][loc[1]]
	for pos in check_2:
		if abs(pos - now_pos)/scale > thresh_grad:
			break
		good += 1
		now_pos = pos 

	return good >= num_squares 

# adapted from
# https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

def findPath(maze, start, end, vehicle, unit):
	"""Returns a list of tuples as a path from the given start to the given end in the given maze"""

	s_u = ''.join(i for i in unit if not i.isalpha())
	if not s_u: s_u = '1'
	clean_unit = float(s_u)

	# Create start and end node
	start_node = Node(None, start)
	start_node.g = start_node.h = start_node.f = 0
	end_node = Node(None, end)
	end_node.g = end_node.h = end_node.f = 0

	# Initialize both open and closed list
	open_list = []
	closed_list = []

	# Add the start node
	open_list.append(start_node)

	# Loop until you find the end
	while len(open_list) > 0:

		# Get the current node
		current_node = open_list[0]
		current_index = 0
		for index, item in enumerate(open_list):
			if item.f < current_node.f:
				current_node = item
				current_index = index

		# Pop current off open list, add to closed list
		open_list.pop(current_index)
		closed_list.append(current_node)

		# Found the goal
		if current_node == end_node:
			path = []
			current = current_node
			while current is not None:
				path.append(current.position)
				current = current.parent
			return path[::-1] # Return reversed path

		# Generate children
		children = []
		for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

			# Get node position
			node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

			# Make sure within range
			if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
				continue

			rise = maze[node_position[0]][node_position[1]] - maze[current_node.position[0]][current_node.position[1]]
			run = clean_unit * 1.4 if new_position[0] != 0 and new_position[1] != 0 else clean_unit

			# Make sure walkable terrain (can we traverse)
			if not vehicle.canTraverse(-np.arctan(rise / run), rise):
				continue

			# Make sure terrain is wide enough to accomodate the vehicle
			if not is_wide_enough(maze, current_node.position, node_position, vehicle, clean_unit):
				continue

			# Create new node
			new_node = Node(current_node, node_position)

			# Append
			children.append(new_node)

		# Loop through children
		for child in children:

			# Child is on the closed list
			for closed_child in closed_list:
				if child == closed_child:
					continue

			# Create the f, g, and h values
			child.g = current_node.g + 1
			child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
			child.f = child.g + child.h

			# Child is already in the open list
			for open_node in open_list:
				if child == open_node and child.g > open_node.g:
					continue

			# Add the child to the open list
			open_list.append(child)
