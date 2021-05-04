# This program accesses info from the Blue's onboard sensor, MPU9250
# It reads temp, accelerometer, gyro, and magnetometer data from the sensor.
# Uses RCPY library.  See guitar.ucsd.edu/rcpy/rcpy.pdf for documentation

# Import external librarires
import time                                     # for time.sleep function
import numpy as np                              # for working with matrices
import rcpy                                     # import rcpy library (this automatically initializes robotics cape)
import rcpy.mpu9250 as mpu9250                  # for mpu sensor functions

rcpy.set_state(rcpy.RUNNING)                    # set state to rcpy.RUNNING
mpu9250.initialize(enable_magnetometer=True)    # by default, mag is not initialized.
mpu9250.initialize()                            # initialize the sensor

def getMag():
    mag = mpu9250.read_mag_data()               # gets x,y,z mag values (microtesla)
    mag = np.round(mag, 1)                      # round values to 1 decimal
    return(mag)

