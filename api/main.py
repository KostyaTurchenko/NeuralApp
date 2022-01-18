import os
from math import *
from PIL import Image
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import base64
import matplotlib.dates as mdates
import datetime as dt
import csv

def predict(path):
    width, height = 250, 250

    if K.image_data_format() == 'channels_first':
        input_shape = (3, width, height)
    else:
        input_shape = (width, height, 3)

    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding="same", input_shape=input_shape, activation='relu'))
    model.add(MaxPooling2D(pool_size=(3, 3)))

    model.add(Conv2D(64, (3, 3), padding="same", activation='relu'))
    model.add(MaxPooling2D(pool_size=(3, 3)))

    model.add(Conv2D(128, (3, 3), padding="same", activation='relu'))
    model.add(MaxPooling2D(pool_size=(3, 3)))

    model.add(Flatten())
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(10))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Prediction
    class_list = os.listdir('data/validation_resize/')
    class_list = sorted(class_list)
    model.load_weights('data/weights.h5')
    img = image.load_img(path, target_size=(250, 250))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x * 1. / 255  # rescale as training
    prediction = model.predict(x)
    values = np.round(prediction, 3)[0]
    plot(class_list, values)
    result = class_list[np.argmax(prediction)]
    print(result)
    sendPredict=[]
    sendPredict.append(result)
    sendPredict.append(class_list)
    sendPredict.append(values)
    print(sendPredict)
    return sendPredict


def plot_value_array(i, predictions_array, true_label):
  true_label = true_label[i]
  plt.grid(False)
  plt.xticks(range(10))
  plt.yticks([])
  thisplot = plt.bar(range(10), predictions_array, color="#777777")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)

  thisplot[predicted_label].set_color('red')
  thisplot[true_label].set_color('blue')

def plot(names,values):
    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 10})

    plt.title('Предсказание')

    xs = range(len(names))

    plt.pie(
        values, autopct='%.1f', radius=1.1,
        explode=[0.15] + [0 for _ in range(len(names) - 1)])
    plt.legend(
        bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
        loc='lower left', labels=names)
    fig.savefig('data/diagrams/pie.png')

def sendImage():
    with open('data/diagrams/pie.png', "rb") as image_file:
        base64string = base64.b64encode(image_file.read())
        return base64string

