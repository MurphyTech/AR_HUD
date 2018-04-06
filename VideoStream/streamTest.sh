#!/bin/bash
IP=$(hostname -I)
# exec the following pipeline (only after gstreamer runs on the client!):
gst-launch-1.0 -vvv -e v4l2src \
 ! video/x-h264,width=480 , height=300 , framerate=30/1 \
 ! gdppay \
 ! udpsink host=192.168.0.143 port=5000
