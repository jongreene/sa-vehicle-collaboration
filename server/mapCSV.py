import numpy as np
import matplotlib.pyplot as plt
import importlib
importlib.import_module('mpl_toolkits.mplot3d').Axes3D

file_name = 'terrain.csv'

terrain = np.genfromtxt(file_name, dtype=float, delimiter=',')

x = range(len(terrain))
y = range(len(terrain[0]))

figure = plt.figure()
surface = figure.add_subplot(111, projection='3d')
X, Y = np.meshgrid(x, y)
surface.plot_surface(X, Y, terrain)

plt.show()