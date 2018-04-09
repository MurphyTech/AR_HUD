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

print "Xbox controller sample: Press Back button to exit"
# Loop until back button is pressed
while not joy.Back():
    # Show connection status
    if joy.connected():
        print "Connected   "
    else:
        print "Disconnected"
        
    while (True):
        (x,y) = joy.leftStick()
        # x = Left-Right
        # y = Up-Down
        magnitude = math.sqrt(x*x + y*y)
        theta = math.atan2(y, x)
        mapRight = 255*magnitude*math.cos(theta)
        mapLeft = 255*magnitude*math.sin(theta)
        
        if y <= 0:
            print 'Backward! Left:{left} Right:{right}'.format(left=int(mapLeft), right=int(mapRight))
            leftMotor.run(Adafruit_MotorHAT.BACKWARD)
            rightMotor.run(Adafruit_MotorHAT.BACKWARD)
        else:
            print 'Forward! Left:{left} Right:{right}'.format(left=int(mapLeft), right=int(mapRight))
            leftMotor.run(Adafruit_MotorHAT.FORWARD)
            rightMotor.run(Adafruit_MotorHAT.FORWARD)

        leftMotor.setSpeed(abs(int(mapLeft)))
        rightMotor.setSpeed(abs(int(mapRight)))
        time.sleep(0.01)

# Close out when done
joy.close()
