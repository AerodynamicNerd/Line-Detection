#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from sensor_msgs.msg import Image, CameraInfo


def talker():
  video_capture = cv2.VideoCapture(0)
  video_capture.set(3,160)
  video_capture.set(4,120)
  font = cv2.FONT_HERSHEY_COMPLEX

  #
  #global contours
  #global val

  while not rospy.is_shutdown():

    rospy.init_node('talker', anonymous=True)

    # Capture frame-by-frame
    ret, frame = video_capture.read()
    _, img = video_capture.read()# find _,

    # Our operations on the frame come here
    if ret:
#    crop_img = frame[60:120, 0:160]
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      blur = cv2.GaussianBlur(hsv,(5,5),0)

    # color Threshold
      ret,thresh = cv2.threshold(hsv,60,120,cv2.THRESH_BINARY_INV)



    # defining the range of yellow/red
      yellow_lower = np.array([22,60,200],np.uint8)
      yellow_upper = np.array([60,255,255],np.uint8)

      #lower_red = np.array([0,50,50])
      #upper_red = np.array([10,255,255])

      yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
      #red = cv2.inRange(hsv, lower_red, upper_red)

      kernal = np.ones((5, 5), "uint8")
      yellow = cv2.dilate(yellow, kernal)
      #red = cv2.dilate(red,kernal)

      res_yellow = cv2.bitwise_and(frame, frame, mask = yellow)
      #res_red = cv2.bitwise_and(frame, frame, mask = red)


    # Frame contours
    #contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
      contours,hierarchy = cv2.findContours(yellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
      #contours,hierarchy = cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

      for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        cv2.drawContours(img, [approx], 0, (0), 5)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        #if len(approx) == 8:
        #  cv2.putText(img, "octagon", (x, y), font, 1, (0))
          #print ("Stop sign in sight")
        #  break

    # Detecting contours
      if len(contours) > 0:

        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        cv2.line(frame,(cx,0),(cx,720),(255,0,0),1)
        cv2.line(frame,(0,cy),(1280,cy),(255,0,0),1)
        cv2.drawContours(frame, contours, -1, (255,128,213), 1)
        #print(2)

        val = String

        if cx >= 130 and cx < 160:
          val = "c1"

        elif cx < 130 and cx >= 86:
          val = "c2"

        elif cx < 86 and cx >= 76:
          val = "c3"

        elif cx < 76 and cx >= 30:
          val = "c4"

        elif cx < 30 and cx > 0:
          val = "c5"

        #elif cx >= 160 and cx <= 0:
        #  val = "c0"
	else:
          val = "c0"
          print ("Nothing found...")

        # Display the resulting frame
        cv2.imshow('frame',frame)
        cv2.imshow('yellow',yellow)
        #cv2.imshow('red',red)
        #cv2.imshow('res_red',res_red)
        cv2.imshow('res_yellow',res_yellow)
        # cv2.imshow('frame',gray)
        #print(1)
        # print(val)

    else:
        val = "c0"
        print ("Nothing found...")

    if cv2.waitKey(1) & 0xFF == ord('q'):
	video_capture.release()
   	cv2.destroyAllWindows()
	break

    pub = rospy.Publisher('chatter', String, queue_size=10)
    pub.publish(val)
    rospy.loginfo(val)

   # When everything done, release the capture
   #video_capture.release()
   #cv2.destroyAllWindows()

if __name__ == '__main__':
  try:
    talker()
  except rospy.ROSInterruptException:
    pass
