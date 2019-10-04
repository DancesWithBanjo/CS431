import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import optimizers
import os, sys, glob
import numpy as np
import cv2

def load_image(file):
    """
    Loads an image file and prepares it for training data
    Also creates an output label

    @file: the image file to prepare
    """
    image = cv2.imread(file)
    image = image.astype('float') / 255.0

    file_name = os.path.split(file)[1]
    if file_name[0] == 'c' : label = np.array((1,0))
    elif file_name[0] == 'd' : label = np.array((0,1))
    else: label = np.array((0,0))

    return (image, label)

def load_images(dir):
    """
    Prepares a directory of images to create an array of training data
    Also creates an array of output labels

    @dir: the directory to pull images from
    """
    training_data = []
    training_labels = []

    for file in glob.glob(dir + '/*.jpg'):
        data, label = load_image(file)
        training_data.append(data)
        training_labels.append(label)

    training_data = np.array(training_data)
    training_labels = np.array(training_labels)

    return (training_data, training_labels)

def make_network(dir, filename):
    """
    Creates a trained neural network using Keras architechture with a directory of training data

    @dir: the directory of training data
    @filename: the name of the outputted dnn file
    """
    training_data, training_labels = load_images(dir)

    model = Sequential()
    model.add(Conv2D(20, (5,5), input_shape=(100, 100, 3), activation = 'relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides = (2,2)))

    model.add(Conv2D(30, (5,5), input_shape=(100, 100, 3), activation = 'relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides = (2,2)))

    model.add(Conv2D(40, (5,5), input_shape=(100, 100, 3), activation = 'relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides = (2,2)))

    model.add(Conv2D(50, (5,5), input_shape=(100, 100, 3), activation = 'relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides = (2,2)))

    model.add(Flatten())
    model.add(Dense(500, activation = 'relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2, activation = 'softmax'))

    model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

    model.fit(training_data, training_labels, batch_size = 100, epochs = 50, verbose = 1)

    scores = model.evaluate(training_data, training_labels)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
    model.save(filename + '.dnn', include_optimizer = False)
    return model

if len(sys.argv) < 2:
    print("Need a file. ")
    sys.exit(1)

make_network(sys.argv[1], sys.argv[2])
