#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
from Tkinter import *
import time

#tkinter

window = Tk()
window.geometry("600x480")
window.title("Servo")

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 500  # Min pulse length out of 4096
servoMax = 600
servoStep = 50  # Max pulse length out of 4096
servoCurrentPan = 0
servoCurrentTilt = 0

def setServoPulse(channel, pulse):
  #pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength = 10000
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

def right(event, servoCurrentPan):
  step = servoCurrentPan + servoStep
  pwm.setPWM(0, servoCurrentPan, step)
  servoCurrentPan = step
  time.sleep(0.01)
  return servoCurrentPan

def left(event):
  step = servoCurrent - servoStep
  pwm.setPWM(0,servoCurrentPan, step)
  servoCurrentPan = step
  time.sleep(0.01)

def up(event):
  pwm.setPWM(1,0,servoMin)
  time.sleep(0.01)

def down(event):
  pwm.setPWM(1, 0, servoMax)
  time.sleep(0.01)

window.bind("<w>", up)
window.bind("<s>", down)
window.bind("<a>", left)
servoCurrentPan = window.bind("<d>", self.right(servoCurrentPan))

window.mainloop()



