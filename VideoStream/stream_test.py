#Script to test opencv with a live video stream
#David Murphy - 12493252

# import necessary packages
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import time

args = 0
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GStreamer stuff
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#url = ""

#cap = cv2.VideoCapture("fdsrc location=http://root:admin@192.1681.120:5000 ! decode ! videoconvert ! appsink")

#cap = cv2.VideoCapture("gst-launch-1.0 -v tcpclientsrc host=192.168.1.120 port=5000  ! gdpdepay !  rtph264depay ! avdec_h264 ! videoconvert ! appsink")

#cap = cv2.VideoCapture("tcpclientsrc host=192.168.1.120 port=5000 ! gdpdepay ! rtph264depay ! video/x-h264, width=1280, height=720, format=YUY2, framerate=49/1 ! ffdec_h264 ! autoconvert ! appsink sync=false")
#url = "gst-launch-1.0 -v tcpclientsrc host=192.168.1.120 port=5000  ! gdpdepay !  rtph264depay ! ffdec_h264 ! videoconvert ! autovideosink sync=false"
#cap = cv2.VideoCapture(url)
#url = "tcpclientsrc host=192.168.1.120 port=5000 ! gdpdepay ! rtph264depay ! video/x-h264, width=1280, height=720, format=YUY2, framerate=49/1 ! ffdec_h264 ! autoconvert ! appsink sync=false"
#print url
#cap = cv2.VideoCapture(url, cv2.CAP_GSTREAMER)

#cap = cv2.VideoCapture("gst-launch-1.0 udpsrc port=5000 ! application/x-rtp ! rtph264depay ! avdec_h264 ! appsink", cv2.CAP_GSTREAMER) #udpsink sync=false !
#cap = cv2.VideoCapture("udp://127.0.0.1:5000",  cv2.CAP_GSTREAMER)
#time.sleep(2)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Capture Choice
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# For testing
# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    leftCap = cv2.VideoCapture(0)
    rightCap = leftCap
else:
    leftCap = cv2.VideoCapture(args["video"])
    rightCap = cv2.VideoCapture(args["video"])

#print cap

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Video PLayback
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

while(leftCap.isOpened() and rightCap.isOpened()):
    retLeft, leftFrame = leftCap.read()
    retRight, rightFrame = rightCap.read()
    small_Left = imutils.resize(leftFrame, width=min(400, leftFrame.shape[1]))
    small_Right = imutils.resize(rightFrame, width=min(400, rightFrame.shape[1]))

    if (retLeft == True and retRight == True):
        # detect people in the image
        (rectsLeft, weightsLeft) = hog.detectMultiScale(leftFrame, winStride=(4, 4), padding=(8, 8), scale=1.05)
        (rectsRight, weightsRight) = hog.detectMultiScale(rightFrame, winStride=(4, 4), padding=(8, 8), scale=1.05)

        # apply non-maxima suppression to the bounding boxes using
        # fairly large overlap threshold to try to maintain overlapping
        # boxes that are still people
        rectsLeft = np.array([[xL, yL, xL + wL, yL + hL] for (xL, yL, wL, hL) in rectsLeft])
        rectsRight = np.array([[xR, yR, xR + wR, yR + hR] for (xR, yR, wR, hR) in rectsRight])

        pickLeft = non_max_suppression(rectsLeft, probs=None, overlapThresh=0.65)
        pickRight = non_max_suppression(rectsRight, probs=None, overlapThresh=0.65)


        # draw the final bounding boxes
        for (xA, yA, xB, yB) in pickLeft:
		          cv2.rectangle(leftFrame, (xA, yA), (xB, yB), (0, 255, 0), 2)


        # Combine Left and Right Frames using numpy
        # Only works when Left and Right frame are same size
        VideoStream_Stereo = np.concatenate((leftFrame, rightFrame), axis=1)
        cv2.imshow('Capture', VideoStream_Stereo)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CleanUp
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

leftCap.release()
rightCap.release()
cv2.destroyAllWindows()
