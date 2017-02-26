import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import sys

import preprocessing as pp

spear = 'data/shakespeare.txt'
spens = 'data/spenser.txt'
tok_words = 'data/spenspear/tokenized_words.json'

def process_text_spear(file_name):
    with open(file_name) as data_file:
        lines = data_file.readlines()

    poem_lines = []

    for i in range(len(lines)):
        if lines[i][0:3] != '   ' and lines[i] != '\n':
            lines[i] = lines[i].lower()
            poem_lines.append(lines[i].strip())

    return '\n'.join(poem_lines)

def process_text_spens(file_name):
    with open(file_name) as data_file:
        lines = data_file.readlines()
    
    poem_lines = []

    for i in range(len(lines)):
        if len(lines[i]) >= 10:
            lines[i] = lines[i].lower()
            poem_lines.append(lines[i].strip())

    return '\n'.join(poem_lines)

def process_words(file_name):
    lines = pp.read_data(file_name)
    max_len = -1
    words = []

    for line in lines:
        for word in line:
            max_len = max(max_len, len(word))
            words.append(word)

    # for i in range(len(words)):
    #     words[i] = words[i] + (max_len - len(words[i])) * ' '

    return words

    return X, y

if __name__ == '__main__':
    # spear_text = process_text_spear(spear)
    # spens_text = process_text_spens(spens)
    # text = spear_text + spens_text
    text = process_words(tok_words)

    words = sorted(list(set(text)))
    word_to_int = dict((c, i) for i, c in enumerate(words))
    int_to_word = dict((i, c) for i, c in enumerate(words))

    n_words = len(text)
    n_vocab = len(words)

    seq_length = 5

    dataX = []
    dataY = []

    for i in range(n_words - seq_length):
        seq_in = text[i:i+seq_length]
        seq_out = text[i+seq_length]
        dataX.append([word_to_int[word] for word in seq_in])
        dataY.append(word_to_int[seq_out])

    n_patterns = len(dataX)

    X = np.reshape(dataX, (n_patterns, seq_length, 1))
    X = X / float(n_vocab)
    y = np_utils.to_categorical(dataY)

    model = Sequential()
    model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
    # model.add(Dropout(0.2))
    model.add(Dense(y.shape[1], activation='softmax'))
    filename = 'weights-improvement-493-0.1677.hdf5'
    model.load_weights(filename)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
                             
    # filepath="weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
    # checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
    # callbacks_list = [checkpoint]

    # model.fit(X, y, nb_epoch=500, batch_size=64, callbacks=callbacks_list)

    start = np.random.randint(0, len(dataX)-1)
    pattern = dataX[start]
    print "\"", ' '.join([int_to_word[value] for value in pattern]), "\""
    # generate characters
    res = []
    for i in range(140):
        x = np.reshape(pattern, (1, len(pattern), 1))
        x = x / float(n_vocab)
        prediction = model.predict(x, verbose=0)
        index = np.argmax(prediction)
        result = int_to_word[index]
        seq_in = [int_to_word[value] for value in pattern]
        res.append(result)
        pattern.append(index)
        pattern = pattern[1:len(pattern)]
    print "\nDone."

    ' '.join(res)
    print res
