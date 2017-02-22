'''
CS155 ShakespeareBot
preprocessing.py
'''

import nltk
# If you've never run nltk before, open up python terminal and type import nltk.
# Then do nltk.download() and a window should pop up. Then click Downlad.
import csv

def tokenize(lines):
    '''
    Tokenize a list of lines. Returns a list of tokenized sentences. Each
    tokenized sentence is a list of tokens (words).

    Output the set of all words to a file to be used as the indices to the
    emission matrix.
    '''
    tokenized_lines = [nltk.word_tokenize(l) for l in lines]

    words = set()
    for line in tokenized_lines:
        for word in line:
            words.add(word)

    with open('words.csv', 'w') as f:
        wr = csv.writer(f, delimiter=',', quotechar='"')
        wr.writerow(list(words))
        f.close()

    return tokenized_lines


def pos_tokenize(tokenized_lines):
    '''
    Tags tokens with parts of speech.
    '''
    return [nltk.pos_tag(l) for l in tokenized_lines]


def main():
    lines = ["Where art thou Muse that thou forget'st so long,",
    "To speak of that which gives thee all thy might?"]
    result = tokenize(lines)
    print result
    result = pos_tokenize(result)
    print result


if __name__ == "__main__":
    main()
