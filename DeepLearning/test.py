import tensorflow as tf
import cv2 
import numpy as np 
frame = cv2.imread("invideo/0/5.jpg")
mean = np.array([123.68, 116.779, 103.939][::1], dtype="float32")

frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
frame = cv2.resize(frame, (224, 224)).astype("float32")
frame -= mean

# make predictions on the frame and then update the predictions
# queue

model = tf.keras.models.load_model("model/model.h5")


preds = model.predict(np.expand_dims(frame, axis=0))[0]

print()
print(preds)
print(np.argmax(preds))