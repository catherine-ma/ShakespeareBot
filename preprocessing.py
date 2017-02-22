'''
CS155 ShakespeareBot
preprocessing.py
'''

from __future__ import division
import nltk, re, pprint
from nltk import word_tokenize
# If you've never run nltk before, open up python terminal and type import nltk.
# Then do nltk.download() and a window should pop up. Then click Downlad.
import csv


WORD_LIST = "words.csv"
DATA_FILE = "data/shakespeare.txt"


def tokenize(lines):
    '''
    Tokenize a list of lines. Returns a list of tokenized sentences. Each
    tokenized sentence is a list of tokens (words). All words are lowercased.

    Output the set of all words to a file to be used as the indices to the
    emission matrix.
    '''
    tokenized_lines = [nltk.word_tokenize(l) for l in lines]
    tokenized_lines = [[word.lower() for word in line] for line in tokenized_lines]

    words = set()
    for line in tokenized_lines:
        for word in line:
            words.add(word.lower())

    write_word_list(words)

    return tokenized_lines


'''
Read and write to the file WORD_LIST.
'''
def write_word_list(words):
    with open(WORD_LIST, 'w') as f:
        wr = csv.writer(f, delimiter=',', quotechar='"')
        wr.writerow(list(words))
        f.close()
def read_word_list():
    with open(WORD_LIST, 'r') as f:
        rd = csv.reader(f, delimiter=',', quotechar='"')
        return [row for row in rd][0]


def pos_tokenize(tokenized_lines):
    '''
    Tags tokens with parts of speech.
    '''
    return [nltk.pos_tag(l) for l in tokenized_lines]


def process_text(file_name):
	with open(file_name) as data_file:
		lines = data_file.readlines()

	poem_lines = []

	for i in range(len(lines)):
		if lines[i][0:3] != '   ' and lines[i] != '\n':
			poem_lines.append(lines[i].strip())

	return poem_lines


def main():
    lines = process_text(DATA_FILE)
    tokenized_lines = tokenize(lines)
    tokpos_lines = pos_tokenize(tokenized_lines)

    print read_word_list()


if __name__ == "__main__":
    main()

