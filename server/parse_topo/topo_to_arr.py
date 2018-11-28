#
# Created: 28 Nov 2018
# File: topo_to_arr
#
# Takes in a topographical map and a scale, parses
# this to a NumPy array where each cell carries a weight
# that is the relative height of cell
#

import os
from skimage import data, io

def parse_topo(file, scale):
    image = io.imread(file)
    for i in image:
        for j in i:
            print(i, j)

if __name__ == '__main__':
    parse_topo('./examples/ex1.jpg', 1)