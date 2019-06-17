import sys, os
import numpy as np
import matplotlib.pyplot as plt
import importlib
importlib.import_module('mpl_toolkits.mplot3d').Axes3D

def mapCSV(csv_file):
	# make sure the file exists and is correct
	if not os.path.isfile(csv_file) or '.csv' not in str(csv_file):
		print('Error: File either does not exist or is not a csv')
		sys.exit()

	# generate a numpy array from the csv with type float
	m1 = np.genfromtxt(csv_file, dtype=float, delimiter=',')

	# return the x, y gradients
	# [gx1, gy1] = np.gradient(m1)

	# print("\nGradient in the 'x direction':")
	# print(gx1)
	# print("\nGradient in the 'y direction':")
	# print(gy1)

	# vehicleMetrics = {'maxPitchSlope': 2, 'maxRollSlope': 2}

	# constructAstarArray(gx1, gy1, vehicleMetrics)

	return m1

def constructAstarArray(xGradientArray, yGradientArray, vehicleMetrics):
	# maybe remove this line, doing this could lead to the vehicle
	# attempting to go forward up a slope it could only traverse
	# horizontally
	# TODO: search for alternative solutions
	#minSlope = min(vehicleMetrics['maxPitchSlope'], vehicleMetrics['maxRollSlope'])

	arr = np.int_([row[:] for row in xGradientArray])

	for i in range(0, len(xGradientArray)):
		for j in range(0, len(xGradientArray[i])):
			# here, 1 = not traversable, 0 = traversable
			arr[i][j] = 1 if (abs(xGradientArray[i][j]) > vehicleMetrics['maxPitchSlope']) or (abs(yGradientArray[i][j]) > vehicleMetrics['maxPitchSlope']) else 0

	print("\nArray given to A*:")
	print(arr)

	print("\nNote: 0 = traversable, 1 = not traversable, for visualization purposes")

def main():
	terrain = mapCSV("../test1-28-terrain.csv")

	x = range(len(terrain))
	y = range(len(terrain[0]))

	figure = plt.figure()
	surface = figure.add_subplot(111, projection='3d')
	X, Y = np.meshgrid(x, y)
	surface.plot_surface(X, Y, terrain)

	plt.show()

if __name__ == '__main__':
	main()
