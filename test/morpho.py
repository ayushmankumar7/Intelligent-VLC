import cv2 
import numpy as np 


cap = cv2.VideoCapture(0)


while True:

    ret, frame = cap.read()
    a =np.ones((5,5), np.uint8)
    bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(bw, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    erosion = cv2.dilate(thresh, a, iterations= 1)    
    openm = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, a)
    cv2.imshow('thr', thresh)
    cv2.imshow('mor', openm)
    cv2.imshow('ero', erosion)
    cv2.imshow('frame', frame)


    if cv2.waitKey(23) == 27:
        break 


cap.release()
cv2.destroyAllWindows()