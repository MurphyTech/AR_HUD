#!/bin/bash
IP=$(hostname -I)
echo $IP
gst-launch-1.0 -v v4l2src ! video/x-raw,width=1280,height=720,framerate=30/1 ! avdec_h264 ! rtph264pay pt=96 config-interval=1 ! udpsink host=192.168.1.90 port=5000
