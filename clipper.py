import cv2 
import numpy as np 


def clip(frame, side):
    if side == "right":
        frame = frame[:, :260, :]
    else:
        frame = frame[:, 400:, :]
    return frame
