
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten
from keras.layers import Conv2D
from keras import optimizers
from keras.utils.np_utils import to_categorical
import numpy as np
import pandas

class Card(object):

    def __init__(self, id, suit):
        self.id = id
        self.suit = suit

    def is_face_card(self):
        if type(self.id) == str:
            return True
        else: return False

class Chip(object):
    # probably wont need this
    def __init__(self, value):
        self.value = value


# card = Card(1, 'spades')
# jack = Card('jack', 'hearts')
# print(card.is_face_card())
# print(jack.is_face_card())

# NOTE When initializing something, you can set the parameters by name
    # EX: card = Card(id = 1, suit = 'spades')

# install tensorflow with pip
    # pip(3) install __

# we need, tensorflow, keras, numpy (for arrays)

# make a function to define the models architechture

def make_network():
    # Setup data
    features = ['S1', 'C1', 'S2', 'C2', 'S3', 'C3', 'S4', 'C4', 'S5', 'C5', 'RANK']
    train_data = pandas.read_csv('training-data.csv', names=features)
    test_data = pandas.read_csv('test-data.csv', names=features)
    num_ranks = 10
    hands = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    hand_name = {
        0: 'Nothing in hand',
        1: 'One pair',
        2: 'Two pairs',
        3: 'Three of a kind',
        4: 'Straight',
        5: 'Flush',
        6: 'Full house',
        7: 'Four of a kind',
        8: 'Straight flush',
        9: 'Royal flush'
    }

    # Split data into cards and card class
    print ('training data: ', train_data)
    card_train = train_data.iloc[:,0:10].as_matrix()
    print ('training matrix: ', card_train)
    rank_train = train_data.iloc[:,10].as_matrix()
    #card_test  = test_data.iloc[:,0:10].as_matrix()
    #rank_test  = test_data.iloc[:,10].as_matrix()

    print(rank_train)
    #print(rank_test)

    card_rank_train = to_categorical(rank_train)
    #card_rank_test = to_categorical(rank_test)


    model = Sequential() # makes new Sequential model (distinct layers)
    model.add(Dense(200, input_shape = (10,), init = 'uniform', activation = 'relu'))
    model.add(Dense(400, init = 'uniform', activation = 'relu'))
    model.add(Dense(200, init = 'uniform', activation = 'relu'))
    model.add(Dense(num_ranks, init = 'uniform', activation = 'softmax'))

    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
    result = model.fit(card_train, card_rank_train, batch_size = 32, epochs = 100, shuffle = True, verbose = 1)
    model.save('player.dnn')
    #show_scores(model, result, card_train, card_rank_train, card_test, card_rank_test)

    loss, accuracy = model.evaluate(card_train, card_rank_train, verbose=0)
    print("Test: accuracy=%f loss=%f" % (accuracy, loss))

    return model

make_network()
