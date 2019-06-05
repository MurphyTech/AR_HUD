#!/usr/bin/python

__author__  = "David Murphy"

from Adafruit_I2C import Adafruit_MotorHAT as i2c 
import xbox
import time
import math
import atexit
import os

os.environ["ROBOTCTRL"] = "ONLINE"

#CONST
ZERO = 0
#Motor Control Constants
FORWARD = i2c.Adafruit_MotorHAT.FORWARD
BACKWARD = i2c.Adafruit_MotorHAT.BACKWARD
RELEASE = i2c.Adafruit_MotorHAT.RELEASE


# create a default object, no changes to I2C address or frequency
mh = i2c.Adafruit_MotorHAT(addr=0x60)
joy = xbox.Joystick()         #Initialize joystick

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    print("Turning motors Off...")
    mh.getMotor(1).run(i2c.Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(i2c.Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(i2c.Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(i2c.Adafruit_MotorHAT.RELEASE)

def getDirection(left, right):
    if left > ZERO:
        print('LEFT > ZERO')
        dirLeft = FORWARD
    elif left < ZERO:
        print('LEFT < ZERO')
        dirLeft = BACKWARD
    else:
        print('LEFT = ZERO')
        dirLeft = RELEASE

    if right > ZERO:
        print('RIGHT > ZERO')
        dirRight = FORWARD
    elif right < ZERO:
        print('RIGHT < ZERO')
        dirRight = BACKWARD
    else:
        print('RIGHT = ZERO')
        dirRight = RELEASE
    

    if (left == right):
        print("Straight")
    elif (left > right):
        print("Right")
    elif (left < right):
        print("Left")
    else:
        print("Unknown")

    return dirLeft, dirRight

def moveMotors(leftSpeed, rightSpeed):
    # Func to control motor movement. 
    print('moveMotors called!')
    # Set Motor Speed
    leftMotor.setSpeed(abs(int(leftSpeed)))
    rightMotor.setSpeed(abs(int(rightSpeed)))
    # Set motor directions
    leftMotor.run(dirLeft)
    rightMotor.run(dirRight)
    time.sleep(0.01)



        
# Clean-up upon exit
atexit.register(turnOffMotors)

# Define motors
leftMotor = mh.getMotor(2)
rightMotor = mh.getMotor(1)

print("Xbox controller sample: Press Back button to exit")
# Loop until back button is pressed
while (True):
    # Show connection status
    if joy.connected():
        print("Connected!")
    else:
        print("Disconnected!")

    if (joy.A()):
        print("Robot primed...")
        Primed = 1
    else:
        print("Robot waiting...")
        Primed = 0
        
    while (Primed):

        if (joy.B()):
            print("Exiting control state...")
            Primed = 0


        # x = Left-Right
        # y = Up-Down
        # Only concerned with the Y-axis
        (_xL, yL) = joy.leftStick()
        (_xR, yR) = joy.rightStick()
        
        #Compute direction for each track
        dirLeft, dirRight = getDirection(yL, yR)
	print('yL: ' + str(yL) + '\tyR: ' + str(yR))
        #Scale controller input to 0-255 for motorHAT speed.
        yL_scaled = math.sqrt(yL * yL)
	yL_scaled = (yL_scaled * 150.00)
        print('yL_scaled: ' + str(yL_scaled))
        yR_scaled = math.sqrt(yR * yR)
	yR_scaled = (yR_scaled * 150.00)
        print('yR_scaled: ' + str(yR_scaled))

        moveMotors(yL_scaled, yR_scaled)

        print("B:", joy.B())

        #Legacy: hardcoded Forward/Back
        #TODO: Find better (more generic way for motor controller)

        #if y <= 0:
        #    print('Backward! Left:{left} Right:{right}'.format(left=nt(mapLeft), right=int(mapRight)))
            #leftMotor.run(Adafruit_MotorHAT.BACKWARD)i
            #rightMotor.run(Adafruit_MotorHAT.BACKWARD)
        #else:
        #    print('Forward! Left:{left} Right:{right}'.format(left=int(mapLeft), right=int(mapRight)))
        

# Close out when done
joy.close()
print("Controller connection closed...")
