#Script to test opencv with a live video stream
#David Murphy - 12493252
import cv2
import numpy as np
#import gst

#url = ""

#cap = cv2.VideoCapture("fdsrc location=http://root:admin@192.1681.120:5000 ! decode ! videoconvert ! appsink")

#cap = cv2.VideoCapture("gst-launch-1.0 -v tcpclientsrc host=192.168.1.120 port=5000  ! gdpdepay !  rtph264depay ! avdec_h264 ! videoconvert ! appsink")

#cap = cv2.VideoCapture("tcpclientsrc host=192.168.1.120 port=5000 ! gdpdepay ! rtph264depay ! video/x-h264, width=1280, height=720, format=YUY2, framerate=49/1 ! ffdec_h264 ! autoconvert ! appsink sync=false")
#url = "gst-launch-1.0 -v tcpclientsrc host=192.168.1.120 port=5000  ! gdpdepay !  rtph264depay ! ffdec_h264 ! videoconvert ! autovideosink sync=false"
#cap = cv2.VideoCapture(url)
url = "tcpclientsrc host=192.168.1.120 port=5000 ! gdpdepay ! rtph264depay ! video/x-h264, width=1280, height=720, format=YUY2, framerate=49/1 ! ffdec_h264 ! autoconvert ! appsink sync=false"
print url
cap = cv2.VideoCapture(url, cv2.CAP_GSTREAMER)
print cap
while(cap.isOpened()):
    print ("OPEN")
    ret, frame = cap.read()

    cv2.imshow('Capture', frame)

    if cv2.waitkey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
