import keras
import os, sys
import numpy as np
import cv2

def classify(net, files):
    """
    Uses a neural network to classify inputed images to either a cat or dog

    @net: the neural network to use for classification
    @files: the input image files to classify
    """
    i = 2
    model = keras.models.load_model(net)

    print ('') # to seperate program output from warnings...

    for file in files:
        images = []

        image = cv2.imread(file)
        image = cv2.resize(image, (100,100))
        image = image.astype('float') / 255.0
        images.append(image)
        images = np.array(images)

        (cat, dog) = model.predict(images)[0]

        if cat > dog:
            print (sys.argv[i], 'is a cat')
        elif dog > cat:
            print (sys.argv[i], 'is a dog')
        else: print (sys.argv[i], 'is a dog')
        i = i+1


if len(sys.argv) < 2:
    print("Need a file. ")
    sys.exit(1)

classify(sys.argv[1], sys.argv[2:])
