
import numpy as np
import tensorflow as tf
from time import sleep
from src.config import HAND_GESTURES
import cv2 
import os 
import vlc_ctrl
import dlib 

#Thread(target = self.show, args =()).start()


def load_graph(path):
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        graph_def = tf.GraphDef()
        with tf.gfile.GFile(path, 'rb') as fid:
            graph_def.ParseFromString(fid.read())
            tf.import_graph_def(graph_def, name='')
        sess = tf.Session(graph=detection_graph)
    return detection_graph, sess


def detect_hands(image, graph, sess):
    input_image = graph.get_tensor_by_name('image_tensor:0')
    detection_boxes = graph.get_tensor_by_name('detection_boxes:0')
    detection_scores = graph.get_tensor_by_name('detection_scores:0')
    detection_classes = graph.get_tensor_by_name('detection_classes:0')
    image = image[None, :, :, :]
    boxes, scores, classes = sess.run([detection_boxes, detection_scores, detection_classes],
                                      feed_dict={input_image: image})
    return np.squeeze(boxes), np.squeeze(scores), np.squeeze(classes)


def predict(boxes, scores, classes, threshold, width, height, num_hands=2):
    count = 0
    results = {}
    for box, score, class_ in zip(boxes[:num_hands], scores[:num_hands], classes[:num_hands]):
        if score > threshold:
            y_min = int(box[0] * height)
            x_min = int(box[1] * width)
            y_max = int(box[2] * height)
            x_max = int(box[3] * width)
            category = HAND_GESTURES[int(class_) - 1]
            results[count] = [x_min, x_max, y_min, y_max, category]
            count += 1
    return results

state = 0

def printing(v, lock):
    global state
    while True:

        with lock:

            u = v.value
        statep = u

        if statep == state:
            print(end = "")
        else:
            print(u)
            state = u
            vlc_actions(state)


def vlc_actions(trigger):
    if trigger == 1:
        os.system("vlc-ctrl volume -0.1")
    if trigger == 2:
        os.system("vlc-ctrl volume +0.1")

    if trigger == 6:
        os.system("vlc-ctrl prev")
    if trigger == 7:
        os.system("vlc-ctrl next")

            
        
def pp(frame, Pause = 0):
    detector = dlib.get_frontal_face_detector()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        
        os.system("vlc-ctrl play")
        Pause = 1

    if Pause == 0:
        
        os.system("vlc-ctrl pause")
    Pause = 0
    