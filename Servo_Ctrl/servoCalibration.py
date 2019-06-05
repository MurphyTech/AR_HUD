#!/usr/bin/python
from Tkinter import *
from Adafruit_I2C import Adafruit_PWM_Servo_Driver as i2c
import time

pwm = i2c.PWM(0x41)
# Set frequency to 60hz, good for servos.
pwm.setPWMFreq(60)

#tkinter
window = Tk()
window.geometry("600x480")
window.title("Servo Calibration")
#window.withdraw()

workingServo = 0
currentValueZero = 200
currentValueOne = 200

def moveServo():
    global workingServo
    global currentValueZero
    global currentValueOne
    if workingServo == 0:
        print("Servo: " + str(workingServo) + "\tValue: " + str(currentValueZero))
        pwm.setPWM(workingServo, 0, currentValueZero)
        time.sleep(0.01)
    elif workingServo == 1:
        print("Servo: " + str(workingServo) + "\tValue: " + str(currentValueOne))        
        pwm.setPWM(workingServo, 0, currentValueOne)
        time.sleep(0.01)

def servoZero(event):
    global workingServo
    workingServo = 0
    print("Servo '0' set")

def servoOne(event):
    global workingServo
    workingServo = 1
    print("Servo '1' set")

def up(event):
    if workingServo == 0:
        global currentValueZero
        currentValueZero += 1
    elif workingServo == 1:
        global currentValueOne
        currentValueOne += 1
    moveServo()

def down(event):
    if workingServo == 0:
        global currentValueZero
        currentValueZero -= 1
    elif workingServo == 1:
        global currentValueOne
        currentValueOne -= 1
    moveServo()
    
frame = Frame(window, width=100, height=100)
frame.bind("<0>", servoZero)
frame.bind("1", servoOne)
frame.bind("<w>", up)
frame.bind("<s>", down)
frame.focus_set()
frame.pack()

window.mainloop()
