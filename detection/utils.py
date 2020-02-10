import numpy as np
import tensorflow as tf
from time import sleep
# from config import HAND_GESTURES
import cv2
import os 
import vlc_ctrl
import dlib


#Flag Configuration
tf.flags.DEFINE_integer("width", 640, "Screen width")
tf.flags.DEFINE_integer("height", 480, "Screen height")
tf.flags.DEFINE_float("threshold", 0.6, "Threshold for score")
tf.flags.DEFINE_float("alpha", 0.3, "Transparent level")

FLAGS = tf.flags.FLAGS


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
    HAND_GESTURES = ["Open", "Closed"]
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

def total_predict(image, graph, sess):
    boxes, scores, classes = detect_hands(image, graph, sess)
    action = 0
    text = ""
    results = predict(boxes, scores, classes, FLAGS.threshold, FLAGS.width, FLAGS.height)
    if len(results) == 1:
        x_min, x_max, y_min, y_max, category = results[0]
        x = int((x_min + x_max) / 2)
        y = int((y_min + y_max) / 2)

        if category == "Open" and x <= FLAGS.width / 3:
            action = 7  # Left jump
            text = "Next Track"
        elif category == "Closed" and x <= FLAGS.width / 3:
            action = 6  # Left
            text = "Prev Track"
        elif category == "Open" and FLAGS.width / 3 < x <= 2 * FLAGS.width / 3:
            action = 5  # Jump
            text = "Jump"
        elif category == "Closed" and FLAGS.width / 3 < x <= 2 * FLAGS.width / 3:
            action = 0  # Do nothing
            text = "Stay"
        elif category == "Open" and x > 2 * FLAGS.width / 3:
            action = 2  # Right jump
            text = "Vol Up"
        elif category == "Closed" and x > 2 * FLAGS.width / 3:
            action = 1  # Right
            text = "Vol Down"
        else:
            action = 0
            text = "Stay"
    else:
        action = 40
    return (action)
    


