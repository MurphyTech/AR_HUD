
#!/usr/bin/python
'''
Servo Control code.
Listens to Android device sensor data input and actuates camera system dual-axiz servos accordingly.

David Murphy
d.murphy53@nuigalway.ie
MECE - 12493252
'''
import os, sys, time
import paho.mqtt.client as mqtt
from Adafruit_I2C import Adafruit_PWM_Servo_Driver as i2c

#Constants file
import constant

#Setup Servo HAT
pwm = i2c.PWM(0x41)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK, Returned code: ",rc)
    else:
        print("Bad connection, Returned code: " ,rc)

    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("servoEvent", 0)
    return

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    timeStamp = time.asctime(time.localtime(time.time()))
    print(msg.topic+" " + str(msg.payload) + " @Time: " + timeStamp)
    panAngle, tiltAngle = str(msg.payload).split(",")
    print type(panAngle)
    print type(tiltAngle)
    servoEvent(float(panAngle), float(tiltAngle), timeStamp)

def on_log(mqttc, obj, level, string):
    print(string)

def servoEvent(panAngle, tiltAngle, timeStamp):
    print("Time: " + str(timeStamp) + "\tPan: " + str(panAngle) + "\tTilt: " + str(tiltAngle))
    print("ZERO: " + str(mapPanServo(panAngle)) + " = " + str(panAngle) + "\tONE: " + str(mapTiltServo(tiltAngle)) + " = " + str(tiltAngle))
    #global pwm
    pwm.setPWM(constant.PANSERVO, constant.ZEROTICK, mapPanServo(panAngle))
    pwm.setPWM(constant.TILTSERVO, constant.ZEROTICK, mapTiltServo(tiltAngle))

def mapPanServo(angle):
    print("mapPanServo")
    # y = 661.3 + (-2.89)*x
    # x = Angle in degrees
    # y = correcponding PWM value
    if angle < 4:
        angle = 4
    if angle > 176:
	angle = 176
    print("Pan:" + str(angle))
    return int(round(constant.YINTERCEPTZERO + (constant.SLOPEZERO * int(round(angle)))))

def mapTiltServo(angle):
    print("mapTiltServo")
    # y = 601.6 + (-2.66)*x
    # x = Angle in degrees
    # y = correcponding PWM value
    if angle < 20:
        angle = 20
    if angle > 176:
       angle = 176
    print("Tilt" + str(angle))
    return int(round(constant.YINTERCEPTONE + (constant.SLOPEONE * int(round(angle)))))

def setupServos():
    #global pwm
    #pwm = i2c.PWM(0x41)
    pwm.setPWMFreq(60)
    pwm.setPWM(constant.PANSERVO, constant.ZEROTICK, constant.PANINITIAL)
    pwm.setPWM(constant.TILTSERVO, constant.ZEROTICK, constant.TILTINITIAL)

def main():
    setupServos()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_log = on_log
    print("Calling connect...")
    client.connect("192.168.1.253", 1883)
    print("After connection attempt")

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt")
        #Cleanup()
        sys.exit(0)
