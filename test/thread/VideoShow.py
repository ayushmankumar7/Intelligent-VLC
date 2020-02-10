from threading import Thread 
import cv2 
from CountsPerSec import CountsPerSec
import dlib 



class VideoShow:


    def __init__(self, frame =None):
        self.frame = frame
        self.stopped = False 

    def start(self):
        Thread(target = self.show, args =()).start()
        return self

    def show(self):
        detector = dlib.get_frontal_face_detector()
        while not self.stopped:
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            faces = detector(gray)

            for face in faces:

                x1 = face.left()
                y1 = face.top()
                x2 = face.right()
                y2 = face.bottom()

                self.frame = cv2.rectangle(self.frame, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.imshow('Video', self.frame)
            if cv2.waitKey(1) == ord('q'):
                self.stopped = True 
    
    def stop(self):
        self.stopped = True