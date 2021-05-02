# This program offers functions for controlling servos on the blue
# servo position is specified by "duty."  If the servo is a continuous
# type, the duty will set the speed instead of the position. 
# Uses rcpy library.  Documentation: guitar.ucsd.edu/rcpy/rcpy.pdf
# PROGRAM REQUIRES SUDO. Last udpated 2020.10.08

# Import external libraries
import time, math
import getopt, sys
import rcpy  # This automatically initizalizes the robotics cape
import rcpy.servo as servo
import rcpy.clock as clock	# For PWM period for servos
import L1_motors as m


# INITIALIZE DEFAULT VARS
duty = 1.5		# Duty cycle (-1.5,1.5 is the typical range)
period = 0.01 	# recommended servo period: 20ms (this is the interval of commands)
ch1 = 1			# select channel (1 thru 8 are available)
ch2 = 2			# selection of 0 performs output on all channels
num = 6

rcpy.set_state(rcpy.RUNNING) # set state to rcpy.RUNNING
srvo1 = servo.Servo(ch1)	# Create servo object
srvo2 = servo.Servo(ch2)
clck1 = clock.Clock(srvo1, period)	# Set PWM period for servos
clck2 = clock.Clock(srvo2, period)

servo.enable()		# Enables 6v rail on beaglebone blue
clck1.start()		# Starts PWM
clck2.start()

def move1(angle):
	srvo1.set(angle)
	
def move2(angle):
	srvo2.set(angle)
	
def loop(num):
	if num == 6:
		move1(0)
		m.MotorL(1)
		m.MotorR(-1)
		time.sleep(1)
		print("Ball 6")
		move1(0.75)
		time.sleep(0.125)
		move1(0)
		time.sleep(1)
	elif num==5:
		print("Ball 5")
		m.MotorL(1)
		m.MotorR(-1)
		time.sleep(1)
		move1(0.75)
		time.sleep(0.125)
		move1(0)
		time.sleep(1)
	elif num==4:
		print("Ball 4")
		m.MotorL(1)
		m.MotorR(-1)
		time.sleep(1)
		move1(0.75)
		time.sleep(0.13)
		move1(0)
		time.sleep(1)
	elif num==3:
		print("Ball 3")
		m.MotorL(1)
		m.MotorR(-1)
		time.sleep(1)
		move1(0.75)
		time.sleep(0.15)
		move1(0)
		time.sleep(1)
	elif num==2:
		print("Ball 2")
		m.MotorL(1)
		m.MotorR(-1)
		time.sleep(1)
		move1(0.75)
		time.sleep(0.15)
		move1(0)
		time.sleep(1)
	elif num==1:
		print("Ball 1")
		m.MotorL(1)
		m.MotorR(-1)
		time.sleep(1)
		move1(0.8)
		time.sleep(0.15)
		move1(0)
		time.sleep(1)
	else:
		print("0 balls left please reload")
		num = 0
		time.sleep(5)
if __name__ == "__main__":
	while True:
		if num == 6:
			move1(0)
			m.MotorL(1)
			m.MotorR(-1)
			time.sleep(1)
			print("Ball 6")
			move1(0.75)
			time.sleep(0.125)
			move1(0)
			num=num-1
			time.sleep(2.5)
		elif num==5:
			print("Ball 5")
			m.MotorL(1)
			m.MotorR(-1)
			time.sleep(1)
			move1(0.75)
			time.sleep(0.125)
			move1(0)
			num=num-1
			time.sleep(2.5)
		elif num==4:
			print("Ball 4")
			m.MotorL(1)
			m.MotorR(-1)
			time.sleep(1)
			move1(0.75)
			time.sleep(0.13)
			move1(0)
			num=num-1
			time.sleep(2.5)
		elif num==3:
			print("Ball 3")
			m.MotorL(1)
			m.MotorR(-1)
			time.sleep(1)
			move1(0.75)
			time.sleep(0.15)
			move1(0)
			num=num-1
			time.sleep(2.5)
		elif num==2:
			print("Ball 2")
			m.MotorL(1)
			m.MotorR(-1)
			time.sleep(1)
			move1(0.75)
			time.sleep(0.15)
			move1(0)
			num=num-1
			time.sleep(2.5)
		elif num==1:
			print("Ball 1")
			m.MotorL(1)
			m.MotorR(-1)
			time.sleep(1)
			move1(0.8)
			time.sleep(0.15)
			move1(0)
			num=num-1
			time.sleep(2.5)
		else:
			print("0 balls left please reload")
			num = 6
			m.MotorL(0)
			m.MotorR(0)
			time.sleep(3)
