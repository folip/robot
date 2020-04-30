from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np
import time
import tensorflow as tf


class Camera:
        def __init__(self):
            self.c = cv2.VideoCapture(0)
        def shoot(self):
            frame = self.c.read()[1]
            self.close()
            return frame
class PA:
    def __init__(self):
        detection_model_path = 'models/haarcascade_frontalface_default.xml'
        emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'

        # hyper-parameters for bounding boxes shape
        # loading models
        self.face_detection = cv2.CascadeClassifier(detection_model_path)
        self.emotion_classifier = load_model(emotion_model_path, compile=False)
        self.graph = tf.get_default_graph()
        self.EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised",
         "neutral"]
    def emotion_dect(self,frame):
        time_start = time.time()
        frame = imutils.resize(frame,width=300)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_detection.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)
        frameClone = frame
        
        if len(faces) > 0:
            faces = sorted(faces, reverse=True,
            key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (fX, fY, fW, fH) = faces
                        # Extract the ROI of the face from the grayscale image, resize it to a fixed 28x28 pixels, and then prepare
                # the ROI for classification via the CNN
            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            with self.graph.as_default():
                preds = self.emotion_classifier.predict(roi)[0]
            emotion_probability = np.max(preds)
            label = self.EMOTIONS[preds.argmax()]
        else:
            print("No face detected.")
            return None

        time_end = time.time()
        print("emotion analyze time cost",time_end - time_start)
        return [self.EMOTIONS,preds,emotion_probability]





class Camera:
        def shoot(self):
            frame = self.c.read()[1]
            self.close()
            return frame
        
        def __init__(self):
            self.c = cv2.VideoCapture(0)
        

        
        def shoot_test(self,src = 'o.jpg'):
            frame = cv2.imread(src)
            return frame

        def close(self):
            self.c.release()
