import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER

wCam, hCam = 640, 480
 
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
# Get frame dimensions
frame_width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH )
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT )

detector = htm.handDetector(detectionCon=0.7)
font = cv2.FONT_HERSHEY_COMPLEX



country = None
flag_name = ''
flag = cv2.imread('flags/IT.jpg')

while not country:
    try:
        # get a color from the user and convert it to RGB
        country = input('Type the name of a country and hit enter: ')
        if country == 'italy': flag_name = 'flags/IT.jpg'
        elif country == 'us': flag_name = 'flags/US.png'
        flag = cv2.imread(flag_name)
    except ValueError:
        # catch colors we don't recognize and go again
        print("whoops I don't know that one")

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    
    
    if len(lmList) != 0:
 
        #Find coordinates for fingers
        thumbX, thumbY = lmList[4][1], lmList[4][2] #thumb finger
        indexX, indexY = lmList[8][1], lmList[8][2] #index finger
        middleX, middleY = lmList[12][1], lmList[12][2] #middle finger
        ringX, ringY = lmList[16][1], lmList[16][2] #ring finger
        pinkyX, pinkyY = lmList[20][1], lmList[20][2] #pinky finger
    
        #Draw cirles for each finger
        cv2.circle(img, (thumbX, thumbY), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (indexX, indexY), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (middleX, middleY), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (ringX, ringY), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (pinkyX, pinkyY), 10, (255, 0, 0), cv2.FILLED)

        #Function to calculate distance given two points
        len_calc = lambda x1,y1,x2,y2: math.hypot(x2 - x1, y2 - y1)
        
        #Calculate various distances
        l_thumb_index = len_calc(thumbX,thumbY,indexX,indexY)
        l_index_middle = len_calc(indexX,indexY,middleX,middleY)
        l_middle_ring = len_calc(middleX, middleY, ringX, ringY)
        l_ring_pinky = len_calc(ringX, ringY, pinkyX, pinkyY)
        l_thumb_ring = len_calc(thumbX,thumbY, ringX, ringY)
                        
        #Recongize gestures
        cosa_fai = l_thumb_index<50\
                    and l_index_middle<50\
                    and l_middle_ring<50\
                    and l_ring_pinky<50\
                    and l_thumb_ring<50
        
        hi_five = l_thumb_index>150\
             and l_index_middle>50\
             and l_middle_ring>50\
             and l_ring_pinky>50\
             and l_thumb_ring>50
        
        ok_sign = l_thumb_index<50\
             and l_index_middle>50\
             and l_middle_ring>50\
             and l_ring_pinky>50\
             and l_thumb_ring>50
        
        phone_sign = l_thumb_index>120\
             and l_index_middle<50\
             and l_middle_ring<40\
             and l_ring_pinky<150\
             and l_thumb_ring>180
        
        peace_sign = l_thumb_index>130\
             and l_index_middle>80\
             and l_middle_ring>140\
             and l_ring_pinky<40\
             and l_thumb_ring<30
        
        print(l_index_middle)
    
        if cosa_fai: cv2.putText(img, 'What are you doing?', (200, 70), font, 1, (255, 255, 255), 3)
        elif hi_five: cv2.putText(img, 'Hi!', (200, 70), font, 1, (255, 255, 255), 3)
        elif ok_sign: cv2.putText(img, 'Ok', (200, 70), font, 1, (255, 255, 255), 3)
        elif phone_sign: cv2.putText(img, 'Call me', (200, 70), font, 1, (255, 255, 255), 3)
        elif peace_sign: cv2.putText(img, 'Peace', (200, 70), font, 1, (255, 255, 255), 3)
    
    flag_h, flag_w, _ = flag.shape
    img[50:50+flag_h, 50:50+flag_w] = flag
    cv2.imshow("Img", img)
    cv2.waitKey(1)