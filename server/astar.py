import math
import random
import numpy as np
import time
import makeDirections
from vehicle import Vehicle

# Disables unnecessary features when running on raspberry pi
running_on_pi = True

if not running_on_pi:
	import cv2 as cv

# OPEN CV CONSTANTS
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


# adapted from
# https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

def astar(maze, start, end, vehicle, unit):
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
			if not vehicle.canTraverse(-np.arctan(rise / run)):
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


def main():

	unit = 'cm'
	power = 5
	mass = 3
	vehicle = Vehicle(power, mass)

	# BEGIN PATHFINDING
	maze = np.genfromtxt('terrain.csv', delimiter=',')
	n = len(maze)
	start = (0, 0)
	end = (n - 1, n - 1)
	timer_start = time.time()
	path = astar(maze, start, end, vehicle, unit)
	timer_end = time.time()
	print("Path found in " + str(round(timer_end - timer_start, 3)) + " seconds")

	print(path)

	makeDirections.makeDirections(path, 1, unit)

	if not running_on_pi:
		# CREATE IMAGE SHOWING PATH THROUGH MAZE
		img = np.zeros((len(maze), len(maze[0]), 3), np.uint8)

		for i in range(n):
			for j in range(n):
				img[i][j] = wall_color if maze[i][j] == 1 else open_color

		for i in range(len(path)):
			if i == 0:
				img[path[i][1],path[i][0]] = start_color
			elif i == len(path) - 1:
				img[path[i][1],path[i][0]] = end_color
			else: 
				img[path[i][1],path[i][0]] = line_color
		cv.imwrite(file_name, img)

		print("Image saved as '" + file_name + "'")

		# END IMAGE CREATION

if __name__ == '__main__':
	main()
