# This example drives the right and left motors.
# Intended for Beaglebone Blue hardware.
# This example uses rcpy library. Documentation: guitar.ucsd.edu/rcpy/rcpy.pdf

# Import external libraries
import rcpy
import rcpy.motor as motor                                     # only necessary if running this program as a loop
import numpy as np                              # for clip function
import L1_adc as adc
dcJackVoltage = 0

motor_l = 1 	                                # Left Motor (ch1)
motor_r = 2 
motor_lw = 3 	                                # Left Motor (ch1)
motor_rw = 4

# NOTE: THERE ARE 4 OUTPUTS.  3 & 4 ACCESSIBLE THROUGH diode & accy functions

rcpy.set_state(rcpy.RUNNING)                    # initialize the rcpy library


# define functions to command motors, effectively controlling PWM
def MotorL(speed):                              # takes argument in range [-1,1]
    motor.set(motor_l, speed)


def MotorR(speed):                              # takes argument in range [-1,1]
    motor.set(motor_r, speed)
    
def MotorLW(speed):                              # takes argument in range [-1,1]
    motor.set(motor_lw, speed)


def MotorRW(speed):                              # takes argument in range [-1,1]
    motor.set(motor_rw, speed)


def diode(state, channel):                      # takes argument in range [0,1]
    np.clip(state, 0, 1)                        # limit the output, disallow negative voltages
    motor.set(channel, state)


def accy(state, channel):                       # takes argument in range [-1,1]
    motor.set(channel, state)
