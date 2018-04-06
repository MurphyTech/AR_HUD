#import socketio
import time
import eventlet
from socketIO_client import SocketIO
import sys
from flask import Flask, render_template

try:
    while True:
        print('Press Ctrl+C to cancle...')
        with SocketIO('http://192.168.0.31', 8088) as socketIO:

            inputVal = raw_input("0 = Pan Servo/ 1 = Tilt Servo\n")
            if inputVal == '0':
                angleVal = raw_input("Angle Value:\n")
                socketIO.emit('servoPanEvent', angleVal)
            if inputVal == '1':
                angleVal = raw_input("Angle Value:\n")
                socketIO.emit('servoTiltEvent', angleVal)
                
            socketIO.wait(seconds=1)

except KeyboardInterrupt:
    print('Concelled!')

socketIO.disconnect()
