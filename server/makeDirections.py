import math
import time

# return a degree that is strictly positive
def normalizeDirection(dir):
	# if dir < 0:
	# 	return int(360 + dir)
	# elif dir == 0.0:
	# 	return 0
	# return int(dir)

	if dir == 0:
		return 0

	return int(dir)

# given a path, make a list of directions with a heading and a length
def makeDirections(path, res, unit, heading=0):
	next_heading = heading
	old_heading = heading
	directions = []

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
			directions[-1] = (normalizeDirection(next_heading), '{}{}'.format(round(float(directions[-1][1].replace(unit, '')) + length, 2), unit))
		else:
			directions.append((normalizeDirection(next_heading) - old_heading, '{}{}'.format(float(length), unit)))
		old_heading = next_heading

	# send directions over ble uart here
	print(directions)