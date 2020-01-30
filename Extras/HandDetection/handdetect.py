import cv2
import numpy as np
import enhance

cap = cv2.VideoCapture(0)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
threshhold = 160
pframes = 1
nframes = 1
while(1):
    ret, frame = cap.read()
    frame = enhance.auto_gamma(frame)
    # frame = cv2.addWeighted(src1=frame, alpha=.5, src2=np.zeros(
    #     frame.shape, frame.dtype), gamma=10, beta=50)

    frame = frame[100:]
    # frame = cv2.normalize(frame, None, alpha=0, beta=1,
    #                       norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(frame, 200, 255, cv2.THRESH_BINARY)
    # thresh = cv2.adaptiveThreshold(
    #     frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 8)

    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    hull = [cv2.convexHull(c) for c in contours]
    try:
        hierarchy = hierarchy[0]
    except:
        hierarchy = []
    height, width = frame.shape
    min_x, min_y = width, height
    max_x = max_y = 0

    for contour, hier in zip(contours, hierarchy):
        (x, y, w, h) = cv2.boundingRect(contour)
        min_x, max_x = min(x, min_x), max(x+w, max_x)
        min_y, max_y = min(y, min_y), max(y+h, max_y)

        if w > 80 and h > 80 and w < 250 and h < 250:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    if max_x - min_x > 0 and max_y - min_y > 0:
        cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)

    cv2.drawContours(frame, hull, -1, (255, 255, 255), thickness=2)
    cv2.imshow("a_img", frame)
    keypress = cv2.waitKey(1) & 0xFF

    if keypress == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
