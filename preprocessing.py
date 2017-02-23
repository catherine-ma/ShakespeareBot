'''
CS155 ShakespeareBot
preprocessing.py
'''

from __future__ import division
import nltk
from nltk import word_tokenize
# If you've never run nltk before, open up python terminal and type import nltk.
# Then do nltk.download() and a window should pop up. Then click Download.
import csv
import json
import string
import re

WORD_LIST = "data/words.csv"
WORD_LIST_JSON = "data/words.json"
ST_FILE = "data/st_words.json"
TOKENIZED_WORDS = "data/tokenized_words.json"
TOKPOS_WORDS = "data/tokpos_words.json"
TOKPOS_POS = "data/tokpos_pos.json"
REVERSE_NUM_TOKENIZED = "data/reverse_num_tokenized.json"
RHYME_PAIRS_NUM = "data/rhyme_pairs_num.json"
STRESS_DICT = "data/stress_dict.json"
NONWORD = "data/nonword.json"
ENDLINE_PUNCTUATION = "data/endline_punctuation.json"

DATA_FILE = "data/shakespeare.txt"
SPENSER_FILE = "data/spenser.txt"

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
    punc = {}
    linecount = 0
    for line in toke_lines:
        new_line = []
        for word in line:
            if word.endswith("'st"):
                new_line.append(word[:-3])
                st_words.append(word[:-3])
            else:
                new_line.append(word)
        new_lines.append(new_line)

        # grab punctuation at the end of the line if exists. Manually exclude
        # close parenthesis as punctuation.
        linecount += 1
        if line[-1] in string.punctuation and line[-1] != ")":
            if line[-1] not in punc:
                punc[line[-1]] = 1
            else:
                punc[line[-1]] += 1
    toke_lines = new_lines

    # get rid of duplicates in st_words
    st_words = list(set(st_words))

    # find unique words and write to word_list file. lowercase them
    words = set()
    for line in toke_lines:
        for word in line:
            words.add(word.lower())

    # Pack up ending punctuation into nice dict
    punctuation = {}
    punctuation['linecount'] = linecount
    punctuation['punc'] = punc

    return toke_lines, words, st_words, punctuation

'''
Read and write to a file ezpz.
'''
def write_word_list(dest, words):
    with open(dest, 'w') as f:
        wr = csv.writer(f, delimiter=',', quotechar='"')
        wr.writerow(list(words))
def read_word_list(dest):
    with open(dest, 'r') as f:
        rd = csv.reader(f, delimiter=',', quotechar='"')
        return [row for row in rd][0]

def write_data(dest, data):
    with open(dest, 'w') as f:
        json.dump(data, f)
def read_data(dest):
    with open(dest, 'r') as f:
        return json.load(f)

def pos_tokenize(tokenized_lines):
    '''
    Tags tokens with parts of speech.
    '''
    cashmeoutsigh = []  # words
    howbowdah = []      # part of speech
    for l in tokenized_lines:
        for tup in nltk.pos_tag(l):
            cashmeoutsigh.append(tup[0])
            howbowdah.append(tup[1])
    return cashmeoutsigh, howbowdah

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

def convert_nonword_json(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)

    new_nonwords = []

    for i in range(len(data)):
        if data[i].isalpha():
            new_nonwords.append(data[i])

    with open('new_nonword.json', 'w') as f:
        json.dump(new_nonwords, f)

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

def process_text(file_name):
    with open(file_name) as data_file:
        lines = data_file.readlines()

    poem_lines = []

    for i in range(len(lines)):
        match = re.match("[MDCLXVI\d]+$", lines[i].strip())
        if not match and lines[i] != '\n':
            if lines[i][0:3] != '   ' and lines[i] != '\n':
                poem_lines.append(lines[i].strip())

    return poem_lines


def get_rhyme_pairs(poems):
    rhyme_pairs = []

    for i in range(len(poems)):
        if len(poems[i]) == 14:
            lw = []

            for line in poems[i]:
                line = line.strip()
                line = line.lower()
                line = line.replace("-", " - ")

                words = nltk.word_tokenize(line)

                if words[-1].isalpha() == False:
                    if words[-2].isalpha() == False:
                        last_word = words[-3]
                    else:
                        last_word = words[-2]
                else:
                    last_word = words[-1]

                if "'st" in last_word:
                    last_word = last_word[-1][:-3]

                lw.append(last_word)

            rhyme_pairs.append((lw[0], lw[2]))
            rhyme_pairs.append((lw[1], lw[3]))
            rhyme_pairs.append((lw[4], lw[6]))
            rhyme_pairs.append((lw[5], lw[7]))
            rhyme_pairs.append((lw[8], lw[10]))
            rhyme_pairs.append((lw[9], lw[11]))
            rhyme_pairs.append((lw[12], lw[13]))

    return rhyme_pairs

def word_to_num(lines, wordset):
    worddict = dict([ (elem, index) for index, elem in enumerate(wordset) ])
    return [[worddict[word] for word in line] for line in lines]

def word_to_num_dict(d, wordset):
    worddict = dict([ (elem, index) for index, elem in enumerate(wordset) ])
    num_d = {}
    for word in d.keys():
        num_d[worddict[word]] = d[word]
    return num_d

def process_data():
    lines = process_text(DATA_FILE)
    # lines = process_text(SPENSER_FILE)
    # lines = process_text('data/sonnet1.txt')
    
    # tokenize
    tokenized_lines, wordset, st_words, punctuation = tokenize(lines)
    # write_data(ST_FILE, st_words)                   # save st words
    # write_data(WORD_LIST, list(wordset))            # save the wordset
    # write_data(TOKENIZED_WORDS, tokenized_lines)    # save the tokenized lines
    # write_data(ENDLINE_PUNCTUATION, punctuation)    # save the endline punc

    # # Find parts of speech
    # tokpos_words, tokpos_pos = pos_tokenize(tokenized_lines)
    # write_data(TOKPOS_WORDS, tokpos_words)  # save words which line up with pos
    # write_data(TOKPOS_POS, tokpos_pos)      # save part of speech
    
    # my_stress_dict, nonwords = create_stress_dict(lines)
    # write_data(STRESS_DICT, my_stress_dict) # save to stressdict
    # write_data(NONWORD, nonwords)           # save to nonwords

    # # reverse every line

    # reverse every line and convert to numbers
    tokenized_lines = [line[::-1] for line in tokenized_lines]
    # num_tokenized_lines = word_to_num(tokenized_lines, wordset)
    # write_data(REVERSE_NUM_TOKENIZED, num_tokenized_lines) # save the thing

    # rhyme
    # poems = process_text_by_poem(DATA_FILE)
    # rhyme_pairs = get_rhyme_pairs(poems)
    # num_rhyme_pairs = word_to_num(rhyme_pairs, wordset)
    # write_data(RHYME_PAIRS_NUM, num_rhyme_pairs)

    # stress
    stress_dict, nonwords = create_stress_dict(tokenized_lines)
    num_stress_dict = word_to_num_dict(stress_dict, wordset)
    write_data(STRESS_DICT, num_stress_dict)
    write_data(NONWORD, list(set(nonwords)))


# This main is for testing purposes only
def main():
    process_data()


if __name__ == "__main__":
    main()

