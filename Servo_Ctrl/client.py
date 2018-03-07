#import socketio
import time
import eventlet
from socketIO_client import SocketIO
import sys
from flask import Flask, render_template

with SocketIO('http://192.168.0.31', 8088) as socketIO:
    text = 90
    text = raw_input("prompt: ")
    print text
    #print (sys.argv)
    socketIO.emit('servoPanEvent', text)
    socketIO.wait(seconds=1)
