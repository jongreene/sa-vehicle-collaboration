import random
import numpy as np
import cv2 as cv

# OPEN CV CONSTANTS
line_width = 3
line_color = (0, 0, 255)
file_name = 'pretty.png'

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

def astar(maze, start, end):
	"""Returns a list of tuples as a path from the given start to the given end in the given maze"""

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

			# Make sure walkable terrain
			if maze[node_position[0]][node_position[1]] != 0:
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

	# GENERATE A MAZE WITH A PATH
	n = 240
	maze = [[0] * n for i in range(n)]

	for i in range(0, len(maze)):
		for j in range(len(maze[i])):
			a = random.randint(1, 10)
			b = random.randint(1, 10)
			maze[i][j] = 1 if a % b == 0 else 0

	# try and make sure that every block isn't completely surrounded 
	for i in range(len(maze)):
		for j in range(len(maze[i])):
			blocked = True
			for next_pos in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]:
				xo = 0
				yo = 0
				if i+next_pos[0] >= n:
					xo = -1 * n
				if j+next_pos[1] >= n:
					yo = -1 *n
				if maze[i+next_pos[0] + xo][j+next_pos[1] + yo] != 1:
					blocked = False 
					break 
			if blocked:
				a = random.randint(-1, 1)
				b = random.randint(-1, 1)
				maze[i+a][j+b] = 0

	# END MAP GENERATE

	start = (0, 0)
	end = (n - 1, n - 1)

	#for row in maze:
	#	print(row)
	
	path = astar(maze, start, end)
	
	#print(path)
	img = np.zeros((len(maze), len(maze[0]), 3), np.uint8)
	print(len(path))
	for i in range(len(path)-1):
		cv.line(img, path[i], path[i+1], line_color, line_width)
	cv.imwrite(file_name, img)

if __name__ == '__main__':
	main()