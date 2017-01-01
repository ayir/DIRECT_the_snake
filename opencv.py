import cv2
import pyautogui
import imutils
import numpy as np
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())
PINK_MIN = np.array([120, 50, 50], np.uint8)
PINK_MAX = np.array([180, 180, 200], np.uint8)
centroid_x = 0
centroid_y = 0
s = ''
move = ''
cnt=''
if not args.get("video", False):
	cap = cv2.VideoCapture(0)
 
# otherwise, grab a reference to the video file
else:
	cap = cv2.VideoCapture(args["video"])
while(cap.isOpened()):

    (ret, img) = cap.read()
    img = cv2.flip(img, 1)

   
    #orig = cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
    img = imutils.resize(img, width=600)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

   
    frame_threshed = cv2.inRange(hsv, PINK_MIN, PINK_MAX)

    
    contours = cv2.findContours(frame_threshed.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    last_x = centroid_x
    last_y = centroid_y

    if contours:
        c = max(contours, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)             
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        M=cv2.moments(c)
        if M["m00"]!=0:
            centroid_x =( int(M["m10"]/M["m00"]))
            centroid_y = (int(M["m01"]/M["m00"]))
        else:
            centroid_x=0
            centroid_y=0
        cv2.circle(img, (centroid_x, centroid_y), 5,(0,0,255),-1)
        cv2.line(img,(400,0),(400,700),(255,0,0),5)
        cv2.line(img,(900,0),(900,700),(255,0,0),5)
        cv2.line(img,(400,350),(900, 350),(255,0,0),5)

            #cv2.imshow('Threshold', frame_threshed)              
    if centroid_x >= 400 and centroid_x <= 900:
        # up
        if centroid_y >= 0 and centroid_y <= 350:
            print('up')
            pyautogui.press('up')
        # down
        if centroid_y >= 350 and centroid_y <=700:
            print ('down')
            pyautogui.press('down')

    # left-right move
    if centroid_y >= 0 and centroid_y <= 700:
        # left
        if centroid_x >= 0 and centroid_x <= 400:
            print ('left')
            pyautogui.press('left')
        # right
        if centroid_x >= 900:
            print ('right')
            pyautogui.press('right')

    cv2.imshow('Original', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord("q"):
	    break
 
# cleanup the camera and close any open windows
cv2.destroyAllWindows()
cap.release()
#cv2.destroyAllWindows(