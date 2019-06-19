import numpy as np
import matplotlib.pyplot as plt
import importlib
importlib.import_module('mpl_toolkits.mplot3d').Axes3D

file_name = 'room_scan.csv'

terrain = np.genfromtxt(file_name, dtype=float, delimiter=',')

terrain = np.flip(terrain, axis=0)

x = range(len(terrain))
y = range(len(terrain[0]))

figure = plt.figure()
surface = figure.add_subplot(111, projection='3d')
X, Y = np.meshgrid(x, y)
surface.plot_surface(X, Y, terrain)

#plt.show()
	# constructAstarArray(gx1, gy1, vehicleMetrics)

	#return m1

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
