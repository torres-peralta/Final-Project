import L1_servo as n
import time, math
import L1_motors as m
num=6

if __name__ == "__main__":
	while True:
		n.loop(num)
		num=num-1
	    