import numpy as np 
import cv2 
import os 
import vlc_ctrl
import dlib 


cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()

os.system("vlc-ctrl play -p /home/ayushman/Documents/cello.mp4")

Pause = 0

try:
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:

            print("Yep")
            os.system("vlc-ctrl play")
            Pause = 1

        if Pause == 0:
            print("Nope")
            os.system("vlc-ctrl pause")
        Pause = 0
	


except KeyboardInterrupt:

    print("GoodBye!")

cap.release()
cv2.destroyAllWindows()
