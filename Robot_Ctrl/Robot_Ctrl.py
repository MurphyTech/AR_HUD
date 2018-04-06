#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import xbox
import time
import math
import atexit

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)
joy = xbox.Joystick()         #Initialize joystick

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

# Clean-up upon exit
atexit.register(turnOffMotors)
# Define motors
leftMotor = mh.getMotor(1)
rightMotor = mh.getMotor(2)

while (True):
    (x,y) = joy.leftStick()
    # x = Left-Right
    # y = Up-Down
    magnitude = sqrt(x^2 + y^2)
    theta = atan2(y, x)
    mapRight = magnitude*cos(theta)
    mapLeft = magnitude*sin(theta)
    
    if y <= 0:
        print "Backward! "
        leftMotor.run(Adafruit_MotorHAT.BACKWARD)
        rightMotor.run(Adafruit_MotorHAT.BACKWARD)
    else:
        print "Forward! "
        leftMotor.run(Adafruit_MotorHAT.FORWARD)
        rightMotor.run(Adafruit_MotorHAT.FORWARD)

    leftMotor.setSpeed(mapLeft)
    rightMotor.setSpeed(mapRight)
    time.sleep(0.01)

joy.close()
