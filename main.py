import numpy as np
import cv2
import os 
import vlc_ctrl

cap = cv2.VideoCapture(0)

os.system("vlc-ctrl play -p /home/ayushman/Documents/cello.mp4")
face_cascade  = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
Pause = 0 
try:
	while True:
		ret , img = cap.read() 
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		for (x, y, w, h) in faces:
			print ("Yep")
			os.system("vlc-ctrl play")
			Pause = 1 
		if Pause == 0: 
			print ("Nope")
			os.system("vlc-ctrl pause")
		Pause = 0 

except KeyboardInterrupt:

	print ("Goodbye!") 

cap.release()
cv2.destoryAllWindows() 