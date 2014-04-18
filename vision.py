#OpenCV code borrowed from www.raspberrypi.org/forums/viewtopic.php?t=46759&p=376737

#hsv stores colors Hue, Saturation, and value
#Hue values of basic colors

    #    Orange  0-22
   #     Yellow 22- 38
    #    Green 38-75
    #    Blue 75-130
     #   Violet 130-160
    #    Red 160-179

import numpy as np
import cv2
import create
import platform
import os

# imported platform module to help with cross-compatibility
if platform.system() == 'Windows':
	r = create.Create(4)
elif platform.system() == 'Linux':
	r = create.Create("/dev/ttyUSB0")
elif platform.system() == 'Darwin'
	r = create.Create("/dev/tty.keySerial1")
else
	print("No supported OS found, exiting!")
	os._exit(1)

# create video capture
cap = cv2.VideoCapture(0)
best_cnt = 0
moveCnt = 0
while(1):
	# poll sensors, and then check if we've hit something
	sensors = r.sensors([create.LEFT_BUMP, create.RIGHT_BUMP])
	# if we hit the left, turn left
	if sensors[create.LEFT_BUMP] == 1:
		r.turn(30)
		moveCnt = 0
	# if we hit the right, turn right
	elseif sensors[create.RIGHT_BUMP] == 1:
		r.turn(-30)
		moveCnt = 0

	# read the frames
	_,frame = cap.read()
	
	# smooth it
	frame = cv2.blur(frame,(3,3))

	# convert to hsv and find range of colors
	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	thresh = cv2.inRange(hsv,np.array((160, 80, 80), dtype=np.uint8), np.array((170, 255, 255), dtype=np.uint8))
	thresh2 = thresh.copy()

	# find contours in the threshold image
	contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	
	# finding contour with maximum area and store it as best_cnt
	max_area = 0
	for cnt in contours:
	    area = cv2.contourArea(cnt)
	    if area > max_area:
	        max_area = area
	        best_cnt = cnt

	# if the max_area of identified color is too small, turn until it's big enough
	# if it's big enough, move towards it 10 centimeters
	if max_area < 50:
		r.turn(30)
		print("Turning!")
		moveCnt = 0
	else:
		r.go(100)
		print("Moving!")
		moveCnt = moveCnt + 1

	print("Move Count: "+str(moveCnt))
	if moveCnt >= 5:
		break

	# if key pressed is 'Esc', exit the loop
	if cv2.waitKey(33)== 27:
	    break
	
# Clean up everything before leaving
cap.release()
# Play a victory song!
r.playSong([(88, 8),(88, 16),(88,16),(84, 8),(88, 16),(91,32),(79,16)])
