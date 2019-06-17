# This implementation is a modified version of https://www.redblobgames.com/pathfinding/a-star/implementation.html

import math
import numpy as np
from vehicle import Vehicle
from queue import PriorityQueue

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

def inBoundsFilter(terrain):
	def b(pos):
		(x, y) = pos
		return 0 <= x < len(terrain) and 0 <= y < len(terrain[0])
	return b

def passableFilter(terrain, pos, vehicle, scale):
	def f(next_pos):
		(x1, y1) = pos
		(x2, y2) = next_pos
		rise = terrain[x2][y2] - terrain[x1][y1]
		run = scale * get_cost(pos, next_pos)
		if terrain[next_pos] == 60:
			print(-np.arctan(rise / run))
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
	bf = inBoundsFilter(terrain)
	results = filter(bf, results)
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

def findPath(maze, start, end, vehicle, unit):
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

	while not frontier.empty():

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
