
#!/usr/bin/python
#from Tkinter import *
from Adafruit_PWM_Servo_Driver import PWM
import time
import socketio
import eventlet
from flask import Flask, render_template

sio = socketio.Server()
app = Flask(__name__, template_folder='template')

servos = {
    0 : {'name' : 'pan', 'angle' : 90},
    1 : {'name' : 'tilt', 'angle' : 90},
}


# Load the main form template on webrequest for the root page
@app.route("/")
def index():
    """Serve the client-side application"""

    # Create a template data dictionary to send any data to the template
    templateData = {
        'title' : 'PiServos'
        }
    # Pass the template data into the template piservos.html and return it to the user
    return render_template('piservos.html', **templateData)

@sio.on('connect')
def connect(sid, environ):
    print('connect', sid)

@sio.on('servoEvent')
def message(sid, panAngle, tiltAngle):
    pwm.setPWM(0, 0, angleMap(int(panAngle)))
    print('PAN: ', int(panAngle))
    pwm.setPWM(1, 0, angleMap(int(tiltAngle)))
    print('TILT: ', int(tiltAngle))

@sio.on('servoPanEvent')
def message(sid, panAngle):
    pwm.setPWM(0, 0, angleMap(int(panAngle)))
    print('PAN: ', int(panAngle))

@sio.on('servoTiltEvent')
def message(sid, tiltAngle):
    pwm.setPWM(1, 0, angleMap(int(tiltAngle)))
    print('TILT: ', int(tiltAngle))

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect', sid)

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 500  # Min pulse length out of 4096
servoMax = 600
servoStep = 50  # Max pulse length out of 4096
servoCurrentPan = 0
servoCurrentTilt = 0

leftPos = 0.5
rightPos = 2.5
middlePos = (leftPos + rightPos)/2 + leftPos

positionList = [leftPos, middlePos, rightPos]
msPerCycle = 1000 / 60


def setServoPulse(channel, pulse):
    """PWM setup"""
    pulseLength = 1000000                   # 1,000,000 us per second
    #pulseLength = 10000
    pulseLength /= 60                       # 60 Hz
    print "%d us per period" % pulseLength
    pulseLength /= 4096                     # 12 bits of resolution
    print "%d us per bit" % pulseLength
    pulse *= 1000
    pulse /= pulseLength
    pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)


print('Moving servo on channel 0, press Ctrl-C to quit...')
left = 122
middle = 366
right = 610

def angleMap(angle):
    return int((round((488.0/180.0),0)*angle) + 122)

@app.route("/<direction>")
def move(direction):
    if direction == 'left':
        print("Left...")
        #Increment Angle
        newAngle = servos[0]['angle'] + 5
        #Check if valid
        if newAngle <= 180:
            pwm.setPWM(0, 0, angleMap(newAngle))
            servos[0]['angle'] = newAngle

    elif direction == 'right':
        print("Right...")
        #Decrement Angle
        newAngle = servos[0]['angle'] - 5
        #Check if valid
        if newAngle >= 0:
            pwm.setPWM(0, 0, angleMap(newAngle))
            servos[0]['angle'] = newAngle

    elif direction == 'up':
        print("Up...")
        #Increment Angle
        newAngle = servos[1]['angle'] + 5
        #Check if valid
        if newAngle <= 180:
            pwm.setPWM(1, 0, angleMap(newAngle))
            servos[1]['angle'] = newAngle

    elif direction == 'down':
        print("Down...")
        #Decrement Angle
        newAngle = servos[1]['angle'] - 5
        #Check if valid
        if newAngle >= 0:
            pwm.setPWM(1, 0, angleMap(newAngle))
            servos[1]['angle'] = newAngle


if __name__ == "__main__":
	#wrap Flask application with socketio's middleware
        app = socketio.Middleware(sio, app)

        #deploy as an eventlet WSGI server
        eventlet.wsgi.server(eventlet.listen(('', 8088)),app)
