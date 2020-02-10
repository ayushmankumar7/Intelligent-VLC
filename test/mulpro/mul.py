import multiprocessing as mp 
import cv2 
import numpy as np 
import dlib 




cap = cv2.VideoCapture(0)

def apply(gray, return_dict):
    detector = dlib.get_frontal_face_detector()
    faces = detector(gray)
    return_dict[faces] = faces

if __name__ == "__main__":
    jo = []
    while True:
        manager = mp.Manager()
        return_dict = manager.dict()

        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        p1 = mp.Process(target = apply, args=(gray, return_dict))
        jo.append(p1)
        p1.start()
        
        for j in jo:
            j.join()
        print(return_dict.values())
        cv2.imshow('fr', frame)

        if cv2.waitKey(10) == 27:
            break 
        
    cap.release()
    cv2.destroyAllWindows()
