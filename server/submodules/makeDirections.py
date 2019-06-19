import math

# given a path, make a list of directions with a heading and a length
def makeDirections(path, unit, heading=0):
	next_heading = heading
	old_heading = heading
	directions = []

	s_u = ''.join(i for i in unit if not i.isalpha())
	if not s_u: s_u = '1'
	res = float(s_u)

	for i in range(len(path)-1):
		curr_pos = path[i]
		next_pos = path[i+1]

		# get next heading
		# avoid division by zero in atan
		if next_pos[1] - curr_pos[1] == 0:
			next_heading = 90 if next_pos[1] - curr_pos[1] < 0 else -90
		else:
			next_heading = math.degrees(math.atan((next_pos[0]-curr_pos[0])/(-(next_pos[1] - curr_pos[1]))))

		# get next length
		length = res if next_heading % 90 == 0 else 1.4 * res

		# add to directions list
		if next_heading == old_heading:
			directions[-1] = (int(next_heading), round(float(directions[-1][1]) + length, 2))
		else:
			directions.append((int(next_heading - old_heading), float(length)))
		old_heading = next_heading

	directions[0] = (directions[0][0], directions[0][1] / 100)

	for i in range(len(directions) - 1, 0, -1):
		directions[i] = (directions[i][0] - directions[i - 1][0], directions[i][1] / 100)

	return directions
