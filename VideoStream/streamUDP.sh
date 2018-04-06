#!/bin/bash
gst-launch-1.0 -v v4l2src device=/dev/video0 ! x264enc pass=qual quantizer=20 tune=zerolatency ! rtph264pay ! udpsink host=127.0.0.1 port=5000
