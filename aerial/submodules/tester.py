##
## Date: March 21, 2019
## Overall Sampling and area mapping file
## Ellis Springe
##

# IMPORTS

import serial
import sys
import time

####################################
### Testing System Class Declaration
####################################


class testSystem:

    # initialization of this class, creates serial connection
    def __init__(self,resolution):
       
        # stepper motor step-to-measurement scaling factor
        self.resolution = resolution
        self.step_total = 65
        self.cm_per_step = 3
        self.grid_size = self.step_total * self.cm_per_step # size in cm
        self.dist_between_points = self.grid_size / (self.resolution - 1)
        self.steps_per_cm = .33333
        self.scale_factor = self.dist_between_points * self.steps_per_cm 
        self.time_factor = 18.0 / self.grid_size # seconds to move 65 steps
        
        # connection details
        self.port = '/dev/ttyS0' #this is for the raspi we used
        self.baud = 115200
        self.parity = serial.PARITY_NONE
        self.stopbits = serial.STOPBITS_ONE
        self.bytesize = serial.EIGHTBITS

        # serial port connection
        try:

            print("[+] Attempting connection to testing system...")
            self.connection = serial.Serial(
                port=self.port,
                baudrate=self.baud,
                parity=self.parity,
                stopbits=self.stopbits,
                bytesize=self.bytesize
            )
            print("[+] Connected to testing system")
            
            self.move_home()

        except (ValueError, serial.SerialException) as e:
           
            print(e)
            print("[-] Could not connect to testing system")
            sys.exit()


    # write command to test structure via serial connection
    def conn_write(self,command):
        
        command = command + "\n"
        self.connection.write(bytearray(command,"utf-8"))


    # wait for the Marlin firmware "ok" ack message, this signifies the command was completed
    def conn_wait(self):
        
        t_end = time.time() + 15 
        ack = ""
        while (ack != b"ok\n"):
            ack = self.connection.readline()
            if time.time() > t_end:
                return False

        return True
        

    # bring all stepper motors back to their origins (home)    
    def move_home(self):
        
        print("[+] Homing X and Z axes...")
        command = "G28"
        while True:
            self.conn_write(command)
            
            # if the sent command is ACK-ed, break, if not resend the command
            if self.conn_wait():
                break
        print("[+] Axes reset")
    

    # move motors to desired position
    def move(self,X,Z):
        scaledX = X * self.scale_factor
        scaledZ = Z * self.scale_factor
        print("[+] Moving to position " + str(scaledX) + " " + str(scaledZ)) 
        command = "G0 X" + str(scaledX) + " Z" + str(scaledZ) 
        while True:
            self.conn_write(command)
            
            # if the sent command is ACK-ed, break, if not resend the command
            if self.conn_wait():
                break

        time.sleep(self.time_factor * self.dist_between_points)

####################################
### Class Declaration End 
####################################
    
