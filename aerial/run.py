##
## Date: March 21, 2019
## Overall Sampling and area mapping file
## Ellis Springe
##

# IMPORTS

# import lidar
# import RPi.GPIO as gpio
import random

###

# CONSTANTS

HEIGHT = 10 # height in feet
CONV = .3048 # FT to Meters conversion
ALTITUDE = HEIGHT * CONV * 1000  # height in centimeters, in practice this should be read from altimeter

###

# gpio.setwarnings(False)
# gpio.setmode(gpio.BOARD)
# gpio.setup(10, gpio.IN, pull_up_down=gpio.PUD_DOWN)


#
# Retrieve depth reading from sensor, button allows for "picture"
#
# Inputs: none
# Returns: int (depth value)
def get_sample():
    #TODO

    # return random.randint(0,2)
    val = 0
    while True:
        if gpio.input(10) == gpio.HIGH:
            val = lidar.get_depth()
        elif val != 0:
            print (val)
            return val
        else:
            continue

#
# Moves the testing stepper motor to next sampling position
#
# Inputs: TODO
# Returns: TODO bool?
def next_pos(prev_pos):
    pass

#
# Compile data samples from terrain
#
# Inputs: int (TODO)
# Returns: TODO
def gather(resolution):

    file = open("terrain.csv","w+")
    for i in range(0,resolution):
        line = str(get_sample())

        for j in range(0,resolution):
            if (i % 2 == 0):
                line = line + ',' + str(get_sample())
            else:
                line = str(get_sample()) + ',' + line
            next_pos(1)
        file.write(line + '\n')




def main():
    #while (True):
    #    print get_sample()
    gather(7)

main()
