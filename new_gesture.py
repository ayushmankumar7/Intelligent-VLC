
import tensorflow as tf
import cv2
import multiprocessing as _mp
from src.utils import load_graph, detect_hands, predict, printing, pp
from src.config import ORANGE, RED, GREEN
import dlib 
import os
from threading import Thread
from enhance import adjust_gamma


tf.flags.DEFINE_integer("width", 640, "Screen width")
tf.flags.DEFINE_integer("height", 480, "Screen height")
tf.flags.DEFINE_float("threshold", 0.6, "Threshold for score")
tf.flags.DEFINE_float("alpha", 0.3, "Transparent level")
tf.flags.DEFINE_string("pre_trained_model_path", "src/pretrained_model.pb", "Path to pre-trained model")

FLAGS = tf.flags.FLAGS


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
            _, frame = cap.read()
            frame = adjust_gamma(frame, gamma=1.5)
            

            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes, scores, classes = detect_hands(frame, graph, sess)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            results = predict(boxes, scores, classes, FLAGS.threshold, FLAGS.width, FLAGS.height)
            #Thread(target = pp, args = (frame,)).start()
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
            cv2.imshow('Detection', frame)
    except KeyboardInterrupt:

        print("GoodBye!")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
