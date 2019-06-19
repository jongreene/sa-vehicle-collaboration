##
## Date: March 21, 2019
## Overall Sampling and area mapping file
## Ellis Springe
##

# IMPORTS

import aerial.submodules.tester as tester 
import aerial.submodules.lidar as lidar
import random
import sys
import numpy
import time

###

# CONSTANTS

RESOLUTION = 28 # 28x28 point grid, still assuming fixed grid size 

###

#
# Writes all terrain values to CSV file
#
# Inputs: terrain integer array
# Returns: none
def write_csv(terrain):
    f = open("terrain.csv",'w+')
    
    for i in range(0,RESOLUTION):
        line = str(terrain[i][0])
        for j in range(1,RESOLUTION):
            line = line + ',' + str(terrain[i][j])
        f.write(line + '\n')


#
# Retrieve depth reading from sensor, button allows for "picture"
#
# Inputs: none
# Returns: int (depth value)
def get_sample():
    
    return lidar.get_depth()
    

#
# Compile data samples from terrain
#
# Inputs: none
# Returns: CSV terrain map
def gather():
    
    # initialize test system and home the axes
    testSystem = tester.testSystem(RESOLUTION)
    time.sleep(5)
    
    # Create static value array
    terrain = numpy.zeros((RESOLUTION,RESOLUTION))
    
    # This is the looping functionality for an S flight pattern
    for i in range(0,RESOLUTION):
        print("Line " + str(i+1)) #added for debugging
        
        for j in range(0,RESOLUTION):
            
            if (i % 2 == 1):
                testSystem.move(RESOLUTION-j-1,i)
                sample = get_sample()
                print("\t[+] Point value: " + str(sample)) # added for debugging
                terrain[i][RESOLUTION-j-1] = sample
            else:
                testSystem.move(j,i)
                sample = get_sample()
                print("\t[+] Point value: " + str(sample)) # added for debugging
                terrain[i][j] = sample
            time.sleep(.5) # maybe not needed
            
    write_csv(terrain)
    # print(terrain) # allows for view of terrain values

