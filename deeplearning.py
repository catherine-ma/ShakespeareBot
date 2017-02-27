import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

import nltk
import preprocessing as pp

toke_lines = 'data/spenspear/tokenized_words.json'
ham = 'hamlet.txt'

def process_text_ham(file_name):
    with open(file_name) as data_file:
        lines = data_file.readlines()

    play_lines = []

    for i in range(len(lines)):
        if '=' not in lines[i] and 'Scene' not in lines[i] \
        and 'ACT' not in lines[i] and lines[i] != '\r\n':
            lines[i] = lines[i].lower()
            lines[i] = lines[i].strip()

            play_lines.append(lines[i])

    return play_lines

def tokenize_ham(lines):
    toke_lines = [nltk.word_tokenize(l) for l in lines]
    
    new_lines = []
    count = 0

    for line in toke_lines:
        new_line = []

        for word in line:
            if word.isalpha:
                new_line.append(word)

        new_lines.append(new_line)

    toke_lines = new_lines

    return toke_lines

def elim_punct(lines):
    no_punct_lines = []

    for line in lines:
        no_punct_line = []

        for word in line:
            if word.isalpha():
                no_punct_line.append(word)

        no_punct_lines.append(no_punct_line)

    return no_punct_lines

def lines_to_words(lines):
    words = []

    for line in lines:
        for word in line:
            words.append(word)

    return words

if __name__ == '__main__':
    # Gets list of words from Hamlet and sonnets
    play_lines = process_text_ham(ham)
    toke_play_lines = tokenize_ham(play_lines)
    no_punct_play_lines = elim_punct(toke_play_lines)
    sonnet_lines = pp.read_data(toke_lines)
    no_punct_sonnet_lines = elim_punct(sonnet_lines)
    lines = no_punct_play_lines + no_punct_sonnet_lines
    text = lines_to_words(lines)

    # Prepare data for model
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
    model.add(Dense(y.shape[1], activation='softmax'))
    filename = 'weights/weights-improvement-249-1.1625.hdf5'
    model.load_weights(filename)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
                             
    # filepath='weights/weights-improvement-{epoch:02d}-{loss:.4f}.hdf5'
    # checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
    # callbacks_list = [checkpoint]

    # model.fit(X, y, nb_epoch=250, batch_size=64, callbacks=callbacks_list)

    start = np.random.randint(0, len(dataX)-1)
    pattern = dataX[start]
    print 'Seed Pattern: ' + ' '.join([int_to_word[value] for value in pattern])
    sonnet_words = []
    for i in range(112):
        x = np.reshape(pattern, (1, len(pattern), 1))
        x = x / float(n_vocab)
        prediction = model.predict(x, verbose=0)
        index = np.argmax(prediction)
        result = int_to_word[index]
        seq_in = [int_to_word[value] for value in pattern]
        sonnet_words.append(result)
        pattern.append(index)
        pattern = pattern[1:len(pattern)]

    sonnet = []
    line = []

    for i in range(112):
        if (i + 1) % 8 == 0:
            sonnet.append(line)
            line = []
        else:
            line.append(sonnet_words[i])

    for i in range(14):
        new_line = ' '.join(sonnet[i])
        new_line = new_line.capitalize()
        sonnet[i] = new_line
        
    print '\n'.join(sonnet)

















