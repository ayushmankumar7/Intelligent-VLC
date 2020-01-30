import numpy as np
import cv2
import platform
import dlib
import enhance
from pynput.keyboard import Key, Controller

keyboard = Controller()

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()

# os.system("vlc-ctrl play -p /home/ayushman/Documents/cello.mp4")

Pause = 0


while True:
    try:
        ret, frame = cap.read()
        adjusted = enhance.adjust_gamma(frame, gamma=1.5)
        gray = cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            keyboard.press(Key.media_play_pause)
            keyboard.release(Key.media_play_pause)
            Pause = 1

        if Pause == 0:
            print("Nope")
            keyboard.press(Key.media_play_pause)
            keyboard.release(Key.media_play_pause)
        Pause = 0

    except KeyboardInterrupt:
        print("GoodBye!")
        break


cap.release()
cv2.destroyAllWindows()
