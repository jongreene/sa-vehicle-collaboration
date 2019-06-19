from math import atan, degrees

# given a path, make a list of directions with a heading and a length
def makeDirections(path, unit, heading=0):
	next_heading = heading
	directions = []

	s_u = ''.join(i for i in unit if not i.isalpha())
	if not s_u: s_u = '1'
	res = float(s_u)

	for i in range(len(path)-1):
		(dy, dx) = path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1]

		# get next heading
		# avoid division by zero in atan
		if dx == 0:
			next_heading = 270 if dy == 1 else 90
		elif dy == 0:
			next_heading = 180 if dx == -1 else 0
		elif dx < 0 and dy < 0:
			next_heading = 180 - degrees(atan(dy / dx))
		elif dx < 0 and dy > 0:
			next_heading = degrees(atan(dy / -dx)) + 180
		else:
			next_heading = 360 + degrees(atan(dy / -dx))

		# get next length
		length = res if next_heading % 90 == 0 else 1.4 * res

		# convert from cm to m
		length /= 100

		# add to directions list
		if len(directions) != 0 and next_heading == directions[-1][0]:
			directions[-1] = (int(next_heading), round(float(directions[-1][1]) + length, 2))
		else:
			directions.append((int(next_heading), float(length)))

	for i in range(len(directions) - 1, 0, -1):
		difference = directions[i][0] - directions[i - 1][0]

		if difference > 180:
			directions[i] = (directions[i][0] - 360, directions[i][1])
		else:
			directions[i] = (difference, directions[i][1])

	return directions
