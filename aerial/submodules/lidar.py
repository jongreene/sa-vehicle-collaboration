##
## Date: March 21, 2019
## LIDAR python file for use with the Garmin Lidar Lite v3 sensor
## Ellis Springe
##

# IMPORTS

import sys
import smbus
import time

# CONSTANTS

dbus = 1
daddr = 0x62

bus = smbus.SMBus(dbus)

HEIGHT = 10 # height in feet
CONV = .3048 # FT to Meters conversion
ALTITUDE = HEIGHT * CONV * 1000  # height in centimeters, in practice this should be read from altimeter


#
# Retrieve depth value from LIDAR I2C register
#
# Inputs: none
# Returns: int (depth value)
def get_depth():
    num = 0

    for i in range(0,4):
        bus.write_byte_data(daddr,0x00,0x04)

        flag = True

        while ( flag ):
            bi = "{0:b}".format(bus.read_byte_data(daddr,0x01))
            if (bi[len(bi)-1] == '0'):
                flag = False

        val = bus.read_i2c_block_data(daddr,0x8f,2)
        num += (val[0] * 256) + val[1]

    return ALTITUDE - (num / 4) - 20
