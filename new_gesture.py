
import tensorflow as tf
import cv2
import multiprocessing as _mp
from src.utils import load_graph, detect_hands, predict, printing, pp
from src.config import ORANGE, RED, GREEN
import dlib 
import os
from threading import Thread
from enhance import adjust_gamma
from VideoShow import VideoShow, putIterationsPerSec
from CountsPerSec import CountsPerSec
from VideoGet import VideoGet



def threadVideoShow(ret, frame):   
  
    video_shower = VideoShow(frame).start()
    cps = CountsPerSec()
    print(cps)
    p = cps.start()
    

    while True:
        
        if not ret or video_shower.stopped:
            video_shower.stop()
            break
            
        frame = putIterationsPerSec(frame, cps.countsPerSec())
        video_shower.frame = frame
        cps.increment()
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
def adjusted_detect_face(img): 
      
    face_img = img.copy() 
      
    face_rect = face_cascade.detectMultiScale(face_img,  
                                              scaleFactor = 1.2,  
                                              minNeighbors = 5) 
      
    for (x, y, w, h) in face_rect: 
        cv2.rectangle(face_img, (x, y),  
                      (x + w, y + h), (255, 255, 255), 10)
          
    return face_img 


tf.flags.DEFINE_integer("width", 640, "Screen width")
tf.flags.DEFINE_integer("height", 480, "Screen height")
tf.flags.DEFINE_float("threshold", 0.6, "Threshold for score")
tf.flags.DEFINE_float("alpha", 0.3, "Transparent level")
tf.flags.DEFINE_string("pre_trained_model_path", "src/pretrained_model.pb", "Path to pre-trained model")

FLAGS = tf.flags.FLAGS
#detector = dlib.get_frontal_face_detector()

def main():
    Pause = 0

    graph, sess = load_graph(FLAGS.pre_trained_model_path)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FLAGS.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FLAGS.height)
    mp = _mp.get_context("spawn")
    v = mp.Value('i', 0)
    lock = mp.Lock()
    
    process = mp.Process(target=printing, args=(v, lock))
    os.system("vlc-ctrl play -p /home/ayushman/Documents/cello.mp4")
    
    process.start()

    try:
        while True:
            key = cv2.waitKey(1)
            if key == ord("q"):
                break
            ret, frame = cap.read()
            f = adjusted_detect_face(frame)
            frame = adjust_gamma(frame, gamma=1.5)           
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes, scores, classes = detect_hands(frame, graph, sess)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            results = predict(boxes, scores, classes, FLAGS.threshold, FLAGS.width, FLAGS.height)
            cv2.imshow('fac', f)
            
            if len(results) == 1:
                x_min, x_max, y_min, y_max, category = results[0]
                x = int((x_min + x_max) / 2)
                y = int((y_min + y_max) / 2)
                cv2.circle(frame, (x, y), 5, RED, -1)

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
                with lock:
                    v.value = action
                cv2.putText(frame, "{}".format(text), (x_min, y_min - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, GREEN, 2)
            else:
                with lock:
                    v.value = 40                
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (int(FLAGS.width / 3), FLAGS.height), ORANGE, -1)
            cv2.rectangle(overlay, (int(2 * FLAGS.width / 3), 0), (FLAGS.width, FLAGS.height), ORANGE, -1)
            cv2.addWeighted(overlay, FLAGS.alpha, frame, 1 - FLAGS.alpha, 0, frame)
            #cv2.imshow('Detection', frame)
    except KeyboardInterrupt:

        print("GoodBye!")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
