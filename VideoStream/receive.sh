#!/bin/bash
gst-launch-1.0 udpsrc port=5000 caps="application/x-rtp" ! application/x-rtp ! rtph264depay ! avdec_h264 ! xvimagesink sync=false
