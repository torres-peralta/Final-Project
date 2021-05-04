# Final_Project.py
# Team Number: 
# Hardware TM: Marinella Torres Perralta
# Software TM: Nicholas Barker
# Date: 04/25

import numpy as np
import time

import L1_adc as adc
import L2_color_target as targeting
import L2_heading as heading
import L1_servo as n
import L1_motors as m
import L2_log as log

string = "N/A"
color_targeted = None                                     # empty variable for storing inputted color 

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
        color_range = np.array([[20, 100, 140], [80, 255, 255]])
    elif color_command.lower() == "pink":
        color_range = np.array([[150, 120, 175], [180, 180, 255]])
    elif color_command.lower() == "blue":
        color_range = np.array([[50, 70, 125], [160, 190, 255]])
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
    
    if initial_heading < (180-45):                              
        new_heading = initial_heading
        while (new_heading < (initial_heading+45)) or (new_heading < -160):
            m.MotorLW(0.6)                                                         # gentle speed for testing program. 0.3 PWM may not spin the wheels.
            m.MotorRW(-0.6)
            new_heading = current_heading()
            log.tmpFile(new_heading, "heading.txt") 
    else:
        new_heading = initial_heading
        final_heading = -180 + (45 - (180-initial_heading))
        while (new_heading+5 >= initial_heading) or (new_heading < final_heading):
            m.MotorLW(0.6)                                                         # gentle speed for testing program. 0.3 PWM may not spin the wheels.
            m.MotorRW(-0.6)
            new_heading = current_heading()
            log.tmpFile(new_heading, "heading.txt") 
    return new_heading


def small_adjustment(theta):                                                        # 5 degree angle adjustment
    initial_heading = current_heading()
    
    if theta > 0:
        if initial_heading < (180-5):
            new_heading = initial_heading
            while (new_heading < (initial_heading + theta)) or (new_heading < -160):
                m.MotorLW(0.6)                                                         # gentle speed for testing program. 0.3 PWM may not spin the wheels.
                m.MotorRW(-0.6)
                new_heading = current_heading()
                log.tmpFile(new_heading, "heading.txt")
        else:
            new_heading = initial_heading
            final_heading = -180 + (5 - (180-initial_heading))
            while (new_heading+5 >= initial_heading) or (new_heading < final_heading):
                m.MotorLW(0.6)                                                         # gentle speed for testing program. 0.3 PWM may not spin the wheels.
                m.MotorRW(-0.6)
                new_heading = current_heading()
                log.tmpFile(new_heading, "heading.txt")
    if theta < 0:
        if initial_heading > (-180+5):
            new_heading = initial_heading
            while (new_heading > (initial_heading -5)) or (new_heading > 160):
                m.MotorLW(-0.6)                                                         # gentle speed for testing program. 0.3 PWM may not spin the wheels.
                m.MotorRW(0.6)
                new_heading = current_heading()
                log.tmpFile(new_heading, "heading.txt")
        else:
            new_heading = initial_heading
            final_heading = 180 - (5 + (-180-initial_heading))
            while (new_heading-5 <= initial_heading) or (new_heading > final_heading):
                m.MotorLW(-0.6)                                                         # gentle speed for testing program. 0.3 PWM may not spin the wheels.
                m.MotorRW(0.6)
                new_heading = current_heading()
                log.tmpFile(new_heading, "heading.txt")
 
def check_camera():
    i = 0
    while(i < 10):
        target = targeting.colorTarget(color_values)                            # grab target x, y, radius
        i = i+1
    try:                                                                        # prevents program error from not finding object in frame
        x = target[0]
        radius = target[2]
        
    except TypeError:                                                           # if color not detected, empty variables
        x = None
        radius = None
        
    return x, radius


dcJackVoltage = adc.getDcJack()                                                 # call the getDcJack function from within L1_adc.py
print("DC Jack Voltage: ", dcJackVoltage) 
shots_remaining = int(input("Enter Initial Number of Shots: "))                                                             # variable for storing number of balls left to fire

while(1):
    ### User Input Block ###
    color_targeted, color_values = recieve_input(color_targeted)
    log.stringTmpFile(color_targeted, "ColorTarget.txt")
    ### Searching for Target Block ###
    x, radius = check_camera()
    
    ##NodeRED
    targetThetaStr="N/A"
    log.stringTmpFile(targetThetaStr, "TargetTheta.txt")
    log.stringTmpFile(targetThetaStr, "InFrame.txt")
    log.stringTmpFile(targetThetaStr, "radius.txt")
    log.tmpFile(shots_remaining, "shots.txt") 
    
    print("Searching for Target...")    
    if x is None:                                                               # no target detected, rotate 45 degrees
        print("No Target Located.")
        rotation_search()
        print("exit loop")
        m.MotorLW(0)
        m.MotorRW(0)
        targetThetaStr="N/A"
        log.stringTmpFile(targetThetaStr, "TargetTheta.txt")
        log.stringTmpFile(targetThetaStr, "InFrame.txt")
        log.stringTmpFile(targetThetaStr, "radius.txt")
    else:                                                                       # target detect, small adjustments
        targetTheta = targeting.horizLoc(x)
        targetThetaStr = str(targetTheta)
        radiusstr = str(radius)
        print("Target Located")
        print("Angle from Center of Target:",targetTheta)
        print("Radius: ", radius)
        TargetIn = "In Frame"
        log.stringTmpFile(targetThetaStr, "TargetTheta.txt")
        log.stringTmpFile(TargetIn, "InFrame.txt")
        log.stringTmpFile(radiusstr, "radius.txt")
        
        if not(targetTheta <= 20 and targetTheta >= -20):                         # large angle offset, re-adjust angle
            print("Small angle Adjustment: ", targetTheta)
            m.MotorLW(0)
            m.MotorRW(0)
            small_adjustment(targetTheta)
            m.MotorLW(0)
            m.MotorRW(0)
        elif targetTheta <= 20 and targetTheta >= -20 and radius <= 55:            # small angle offset, drive closer
            print("Driving to Target: ", radius)
            m.MotorLW(0.6)
            m.MotorRW(0.6)
        elif targetTheta <= 20 and targetTheta >= -20 and radius >= 55:                                                                   # small angle offset, within range
            m.MotorLW(0.0)
            m.MotorRW(0.0)
            print("Eliminating Target...")
            while(x is not None):
                if shots_remaining > 0:
                    n.loop(shots_remaining)
                    shots_remaining=shots_remaining-1
                else:
                    shots_remaining = int(input("No shots remaining. Input number of shots added -> "))
                x, radius = check_camera()
                print("x:", x, "radius: ", radius)
                if (x is None):
                    color_targeted = None
                log.tmpFile(shots_remaining, "shots.txt")           
    ###Ending Program ###
    