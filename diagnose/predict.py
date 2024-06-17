import os
import cv2
import numpy as np
import tensorflow as tf

disease = {0:"Normal", 1:"Covid-19", 2:"Viral Pneumonia", 3:"Lung Opacity", 4:"Bacterial Pneumonia"}

#current_file_path
cur = os.path.abspath(__file__).replace('\\', '/')

model_path = cur[:-11] + '/all_diseases_2.h5'
model = tf.keras.models.load_model(model_path)


def predict(img):
  images = []
  if img is None:
      return 'None From predicat'
  img = img / 255.0
  img = cv2.resize(img, (100, 100))
  images.append(img)
  img = np.asarray(images)
  y_pred = model.predict(img)
  return disease[np.argmax(y_pred[0])]
