##
## Date: March 21, 2019
## Overall Sampling and area mapping file
## Ellis Springe
##

# IMPORTS

import tester
import lidar
import RPi.GPIO as gpio
import random
import sys
import numpy
import time

###

# CONSTANTS

HEIGHT = 10 # height in feet TODO
CONV = .3048 # FT to Meters conversion
ALTITUDE = HEIGHT * CONV * 1000  # height in centimeters, in practice this should be read from altimeter

RESOLUTION = int(sys.argv[1]) # maybe fix?

###

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(15, gpio.IN, pull_up_down=gpio.PUD_DOWN)



#
# 
#
# Inputs: TODO
# Returns: TODO bool?
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
    
    #val = 0
    #while True:
    #    if gpio.input(15) == gpio.HIGH:
    #        val = lidar.get_depth()
    #    elif val != 0:
    #        print ("Point  , " + str(val))
    #        return val
    #    else:
    #        continue


#
# Compile data samples from terrain
#
# Inputs: int (TODO)
# Returns: TODO
def gather():
    
    # initialize test system and home the axes
    testSystem = tester.testSystem(RESOLUTION)
    time.sleep(5)
    
    terrain = numpy.zeros((RESOLUTION,RESOLUTION))
    for i in range(0,RESOLUTION):
        print("Line " + str(i+1))
        #line = str(get_sample())
        
        #r = range(1,RESOLUTION)
        #if i%2 == 0:
        #    r = range(1,RESOLUTION,-1)
        
        for j in range(0,RESOLUTION):
            #sample = 1
            #sample = get_sample()
            if (i % 2 == 1):
                testSystem.move(RESOLUTION-j-1,i)
                sample = get_sample()
                print("\t[+] Point value: " + str(sample))
                #print("G0 X" + str(j) + " Z" + str(RESOLUTION-i-1)) 
                #print("I:" + str(i+1) + " J:" +str(RESOLUTION-j))
                terrain[i][RESOLUTION-j-1] = sample
            else:
                testSystem.move(j,i)
                sample = get_sample()
                print("\t[+] Point value: " + str(sample))
                #print("G0 X" + str(j) + " Z" + str(i)) 
                #print("I:" + str(i+1) + " J:" +str(j+1))
                terrain[i][j] = sample
            time.sleep(.5)
            #print(terrain)
            
            
            #print("I:" + str(i+1) + " J:" +str(j+1))
            #if (i % 2 == 0):
            #    line = line + ',' + str(get_sample())
            #else:
            #    line = str(get_sample()) + ',' + line
            #next_pos(1)
        #file.write(line + '\n')

    write_csv(terrain)
    print(terrain)




def main():
    #while (True):
    #    print get_sample()
    gather()

main()
