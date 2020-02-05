import cv2 
import numpy as np 
import os 

m = int(input("Enter Class : 1, 2, 3 or 4(neg) : "))


cap = cv2.VideoCapture(0)

i = 0
j = 0
while True:
    
    ret, frame = cap.read()

    frame = cv2.resize(frame, (480,480))
    if m == 1:
        i += 1
        filename = "invideo/0/"+str(i)+".jpg"
        cv2.imwrite(filename, frame)

    elif m == 2:
        i += 1
        filename = "invideo/0/"+str(i)+".jpg"
        cv2.imwrite(filename, frame)

    elif m == 3:
        i += 1
        filename = "invideo/0/"+str(i)+".jpg"
        cv2.imwrite(filename, frame)

    elif m == 4:
        i += 1
        filename = "invideo/0/"+str(i)+".jpg"
        cv2.imwrite(filename, frame)

        

    cv2.imshow('frame', frame)

    if cv2.waitKey(25) == 27:
        break 

cap.release()
cv2.destroyAllWindows()

