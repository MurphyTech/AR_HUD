#!/bin/bash
#gst-launch-1.0 -v tcpclientsrc host=192.168.1.120 port=5000  ! gdpdepay !  rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false
gst-launch-1.0 -v tcpclientsrc host=192.168.1.120 port=5000 ! gdpdepay ! rtph264depay ! video/x-h264, width=1280, height=720, format=YUY2, framerate=49/1 ! ffdec_h264 ! autoconvert ! appsink sync=false
