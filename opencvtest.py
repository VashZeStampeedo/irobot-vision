import cv2
import numpy as np

# create video capture
cap = cv2.VideoCapture(0)

best_cnt = 0

while(1):

    # read the frames
    _,frame = cap.read()

    # smooth it
    frame = cv2.blur(frame,(3,3))

    # convert to hsv and find range of colors
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv,np.array((160, 50, 50),np.uint8), np.array((180, 255, 255),np.uint8))
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

  

    # Show it, if key pressed is 'Esc', exit the loop
    cv2.imshow('frame',frame)
    cv2.imshow('thresh',thresh2)
    if cv2.waitKey(33)== 27:
        break

# Clean up everything before leaving
cv2.destroyAllWindows()
cap.release()
