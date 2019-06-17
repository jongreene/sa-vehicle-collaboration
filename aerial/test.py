##
## Date: March 21, 2019
## Overall Sampling and area mapping file
## Ellis Springe
##

# IMPORTS

import lidar
import RPi.GPIO as gpio
import random
import serial
import sys
import time
###

# CONSTANTS


ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)


f = open('gcode','r').readlines()

#ser.write(b"M107\n")
#ser.write(b"M28\n")

#bytez1 = "G0 Z%s\n"%(sys.argv[1])
#bytez2 = "G28 Z\n"
#ser.write(bytearray(bytez1,'utf-8'))

while 1:
    b = input("Enter a command: ")
    b += '\n'
    ser.write(bytearray(b,'utf-8'))
    line = ser.readline().decode('utf-8')
    print(line)
    time.sleep(2)

#ser.write(b"G28\n")
#time.sleep(30)

#for line in f:
    #bytez = "G0 X%s\n"%(sys.argv[1])
#    l = line + '\n'
#    ser.write(bytearray(line,'utf-8'))
#    time.sleep(1)


