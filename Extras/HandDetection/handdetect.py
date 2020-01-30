import cv2
import numpy as np
import enhance

cap = cv2.VideoCapture('paper.mp4')

frames = 1
threshhold = 160
while(1):
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    # frame = enhance.auto_gamma(frame)
    frame = cv2.blur(frame, (1, 1))

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(frame, 190, 255, cv2.THRESH_BINARY)

    # contours, hierarchy = cv2.findContours(
    #     thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # hull = [cv2.convexHull(c) for c in contours]
    # try:
    #     hierarchy = hierarchy[0]
    # except:
    #     hierarchy = []
    # height, width = frame.shape
    # min_x, min_y = width, height
    # max_x = max_y = 0

    # for contour, hier in zip(contours, hierarchy):
    #     (x, y, w, h) = cv2.boundingRect(contour)
    #     min_x, max_x = min(x, min_x), max(x+w, max_x)
    #     min_y, max_y = min(y, min_y), max(y+h, max_y)

    #     if w > 80 and h > 80:
    #         cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # if max_x - min_x > 0 and max_y - min_y > 0:
    #     cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)
    frame = frame[300:-500, :]
    frame = cv2.resize(frame, (300, 600))
    frame = cv2.equalizeHist(frame)

    cv2.imshow("a_img", frame)
    keypress = cv2.waitKey(1) & 0xFF
    cv2.imwrite('images/paper' + str(frames) + '.jpg', frame)
    frames += 1
    if keypress == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
