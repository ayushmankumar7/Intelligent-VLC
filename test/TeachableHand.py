import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2



state = 0

labels = ["Point", "Full", "Nothing", "Swing"]
camera = cv2.VideoCapture(0)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5')
while(1):
    ret, frame = camera.read()
    image = cv2.resize(frame, (224, 224))
    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # resize the image to a 224x224 with the same strategy as in TM2:
    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    # image = ImageOps.fit(image, size, Image.ANTIALIAS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # display the resized image
    # image.show()

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    cv2.imshow("image", image)

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    # image_array = np.expand_dims(image_array, axis=0)
    prediction = model.predict(data)
    
    pred = np.argmax(prediction)
    statep = pred
    if statep == state:
        print(end = "")
    else:

        print(labels[pred])
        state = pred
    keypress = cv2.waitKey(400) & 0xFF
    if keypress == ord("q"):
        break
camera.release()
cv2.destroyAllWindows()
