import numpy as np 
import cv2 
import dlib 

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()

while True:

    _,frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    for face in faces:

        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        
        frame = cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(25) == 27:
        break 

cap.release()
cv2.destroyAllWindows()