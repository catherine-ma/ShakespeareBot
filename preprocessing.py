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
    tokenized sentence is a list of tokens (words).

    All words are lowercased.
    Hyphenated words are split into three words (word, hyphen, word).
    Words with past tense 'st at the end have 'st removed and word stored for
    later postprocessing.

    Output the set of all words to a file to be used as the indices to the
    emission matrix.
    '''
    # lowercase everything
    lines = [line.lower() for line in lines]
    # split hyphenated words into three words
    lines = [line.replace("-", " - ") for line in lines]
    
    toke_lines = [nltk.word_tokenize(l) for l in lines]
    
    # words ending in "'st" such as frown'st.
    new_lines = []
    st_words = []
    for line in toke_lines:
        new_line = []
        for word in line:
            if word.endswith("'st"):
                new_line.append(word[:-3])
                st_words = word[:-3]
            else:
                new_line.append(word)
        new_lines.append(new_line)
    toke_lines = new_lines

    ### TODO: do some postprocessing with st_words somewhere

    # find unique words and write to word_list file
    words = set()
    for line in toke_lines:
        for word in line:
            words.add(word.lower())

    write_word_list(words)

    return toke_lines


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


def process_text_by_line(file_name):
    with open(file_name) as data_file:
        lines = data_file.readlines()

    poem_lines = []

    for i in range(len(lines)):
        if lines[i][0:3] != '   ' and lines[i] != '\n':
            poem_lines.append(lines[i].strip())

    return poem_lines

def create_stress_dict(poem_words):
    stress_dict = nltk.corpus.cmudict.dict()
    my_stress_dict = {}
    nonwords = []

    for i in range(len(poem_words)):
        for word in poem_words[i]:
            if word not in stress_dict.keys():
                nonwords.append(word)
            else:
                my_stress_dict[word] = stress_dict[word]

    for word in my_stress_dict.keys():
        phoneme = my_stress_dict[word][0]
        syls = []

        for phon in phoneme:
            if '0' in phon:
                syls.append(0)
            elif '1' in phon:
                syls.append(1)

        my_stress_dict[word] = syls

    return my_stress_dict, nonwords

def process_text_by_poem(file_name):
    with open(file_name) as data_file:
        lines = data_file.readlines()

    poems = []
    poem = []

    for i in range(len(lines)):
        if lines[i][0:3] == '\n':
            if poem != []:
                poems.append(poem)
                poem = []
        elif lines[i][0:3] != '   ' and lines[i] != '\n':
            poem.append(lines[i].strip())

    poems.append(poem)
    return poems

def process_text(poem):
    for i in range(len(poems)):
        if lines[i][0:3] != '   ' and lines[i] != '\n':
            poem_lines.append(lines[i].strip())

    return poem_lines


def get_rhyme_pairs(poems):
    rhyme_pairs = []

    for i in range(len(poems)):
        if len(poems[i]) == 14:
            lw = []

            for line in poems[i]:
                words = line.split(' ')
                last_word = words[-1]

                if last_word[-1].isalpha() == False:
                    last_word = last_word[:-1]

                lw.append(last_word)

            rhyme_pairs.append((lw[0], lw[2]))
            rhyme_pairs.append((lw[1], lw[3]))
            rhyme_pairs.append((lw[4], lw[6]))
            rhyme_pairs.append((lw[5], lw[7]))
            rhyme_pairs.append((lw[8], lw[10]))
            rhyme_pairs.append((lw[9], lw[11]))
            rhyme_pairs.append((lw[12], lw[13]))

    return rhyme_pairs


def main():
    lines = process_text_by_line(DATA_FILE)
    #tokenized_lines = tokenize(lines)
    #tokpos_lines = pos_tokenize(tokenized_lines)
    #my_stress_dict, nonwords = create_stress_dict(lines)
    #poems = process_text_by_poem(DATA_FILE)
    #rhyme_pairs = get_rhyme_pairs(poems)
    #print read_word_list()


if __name__ == "__main__":
    main()

