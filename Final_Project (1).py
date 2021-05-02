# Final_Project.py
# Team Number: 
# Hardware TM: Marinella Torres Perralta
# Software TM: Nicholas Barker
# Date: 04/25

import L0_mjpg_streamer_filter as streamer
import L1_adc as adc
import L2_color_target as targeting
import L2_heading as heading
import L2_kinematics as kinematics
import L2_inverse_kinematics as inverse_kinematics
import L2_speed_control as speed_control
import L1_servo as n
import time, math
import L1_motors as m
num=6

import numpy as np
import time
import math

color_targeted = None                                     # empty variable for storing inputted color 
shots_remaining = 5                                       # variable for storing number of balls left to fire
color_values = np.array([[0, 0, 0], [255, 255, 255]])     # variable for storing HSV of target color

#Recieve viable color input, and assign predetermiend color ranges
def recieve_input(color_target): 
    color_command = color_target
    if color_command == None:                                                 #check if SCUTTLE has target color
        color_command = input("Enter color of target to terminate -> ") 
        while color_command.lower() not in ["green", "blue", "pink"]:
            print("Invalid target. Please try again.\n")
            color_command = input("Enter color of target to terminate -> ")
    
    if color_command.lower() == "green":
        color_range = np.array([[20, 100, 80], [55, 255, 200]])
    elif color_command.lower() == "pink":
        color_range = np.array([[155, 100, 65], [190, 190, 255]])
    elif color_command.lower() == "blue":
        color_range = np.array([[95, 100, 65], [170, 215, 255]])
    return color_command, color_range

def current_heading():
    axes = heading.getXY()                              # call xy function
    axesScaled = heading.scale(axes)                    # perform scale function
    h = heading.getHeading(axesScaled)                  # compute the heading
    headingDegrees = round(h*180/np.pi, 2)
    return headingDegrees

# Rotates SCUTTLE 45 degrees to search for target
def rotation_search(): 
    initial_heading = current_heading()
    de_dt = np.zeros(2)
    
    if initial_heading < (180-45):                              
        new_heading = initial_heading
        while new_heading < (initial_heading+45):
            m.MotorLW(0.78)                         # gentle speed for testing program. 0.3 PWM may not spin the wheels.
            m.MotorRW(-0.78)
            new_heading = current_heading()
            print("No Overflow. Heading: ", new_heading)
    else:
        new_heading = initial_heading
        final_heading = -180 + (180-initial_heading)
        while new_heading >= initial_heading or new_heading < final_heading:
            m.MotorLW(0.78)                         # gentle speed for testing program. 0.3 PWM may not spin the wheels.
            m.MotorRW(-0.78)
            new_heading = current_heading()
            print("Overlow. Heading:", new_heading)
        return


dcJackVoltage = adc.getDcJack()                                     # call the getDcJack function from within L1_adc.py
print("DC Jack Voltage: ", dcJackVoltage) 
streamer.init_filter()

while(1):
    ### User Input Block ###
    color_targeted, color_values = recieve_input(color_targeted)
       
    ### Searching for Target Block ###
    target = targeting.colorTarget(color_values)                    # grab target x, y, radius
    try:                                                            # prevents program error from not finding object in frame
        x = target[0]
        radius = target[2]
    except TypeError: #if color not detected, empty variables
        x = None
        radius = None
        
    if x is None:
        print("no target located.")
        rotation_search()
    else:
        targetTheta = targeting.horizLoc(x)
        print(targetTheta)
        n.loop(num)
        num=num-1
        	
    print("exit loop")
    m.MotorLW(0)
    m.MotorRW(0)
    time.sleep(10)
    
    
    
    ### Shooting Target Block ###
    
    
    
    ###Ending Program ###
    