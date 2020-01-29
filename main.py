import numpy as np 
import cv2 
import os 
import vlc_ctrl
import dlib 
import enhance

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()

os.system("vlc-ctrl play -p /home/ayushman/Documents/cello.mp4")

Pause = 0


while True:
    try:
        ret, frame = cap.read()
        adjusted = enhance.adjust_gamma(frame, gamma= 1.5)
        gray = cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY)
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
        break

    

cap.release()
cv2.destroyAllWindows()