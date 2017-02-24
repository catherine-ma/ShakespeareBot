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
import os
import sys

WORD_LIST_JSON = "words.json"
ST_FILE = "st_words.json"
TOKENIZED_WORDS = "tokenized_words.json"
TOKPOS_WORDS = "tokpos_words.json"
TOKPOS_POS = "tokpos_pos.json"
REVERSE_NUM_TOKENIZED = "reverse_num_tokenized.json"
RHYME_PAIRS_NUM = "rhyme_pairs_num.json"
STRESS_NUM = "stress_num.json"
STRESS_DICT = "stress_dict.json"
NONWORD = "nonword.json"
ENDLINE_PUNCTUATION = "endline_punctuation.json"
NUM_TO_WORD_DICT = "num_to_word_dict.json"
BEE_HARDCODED_RHYMES = "bee_hardcoded_rhymes.json"

DATA_FILE = os.path.join("data", "shakespeare.txt")
SPENSER_FILE = os.path.join("data", "spenser.txt")
BEE_RAW_FILE = os.path.join("data", "bee_raw.txt")
BEE_FILE = os.path.join("data", "bee.txt")

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
    words = list(words)
    numtoworddict = {}
    for i, w in enumerate(words):
        numtoworddict[i] = w

    # Pack up ending punctuation into nice dict
    punctuation = {}
    punctuation['linecount'] = linecount
    punctuation['punc'] = punc

    return toke_lines, words, st_words, punctuation, numtoworddict

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
        # If its a number or a Roman Numeral, then it must be a title row
        match = re.match("[MDCLXVI\d]+$", lines[i].strip())
        if not match and lines[i] != '\n':
            poem_lines.append(lines[i].strip())

    return poem_lines


def process_bee_text(file_name):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    fp = open(file_name)
    data = fp.read()
    lines = tokenizer.tokenize(data)
    with open(BEE_FILE, 'w') as f:
        for l in lines:
            f.write(l + "\n")


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


def get_rhyme_pairs_bee(DEST, wordset):
    rhyme_pairs = []
    # for i, w in enumerate(wordset):
    #     print str(i) + ": word = " + w
    #     if doTheyRhyme("party", w):
    #         rhyme_pairs.append(("bee", w))
    #         print w
    rhymes = read_data(os.path.join(DEST, BEE_HARDCODED_RHYMES))
    for r in rhymes:
        rhyme_pairs.append(("bee", r))
    return rhyme_pairs

def rhyme(inp, level):
    '''
    Taken off of stackoverflow
    http://stackoverflow.com/questions/25714531/find-rhyme-using-nltk-in-python
    '''
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    for (word, syllable) in syllables:
            rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
    return set(rhymes)


def doTheyRhyme ( word1, word2 ):
    '''
    Taken off of stackoverflow
    http://stackoverflow.com/questions/25714531/find-rhyme-using-nltk-in-python
    '''
    # first, we don't want to report 'glue' and 'unglue' as rhyming words
    # those kind of rhymes are LAME
    if word1.find ( word2 ) == len(word1) - len ( word2 ):
        return False
    if word2.find ( word1 ) == len ( word2 ) - len ( word1 ): 
        return False
    return word1 in rhyme ( word2, 1 )


def word_to_num(lines, wordset):
    worddict = dict([ (elem, index) for index, elem in enumerate(wordset) ])
    return [[worddict[word] for word in line] for line in lines]

def word_to_num_dict(d, wordset):
    worddict = dict([ (elem, index) for index, elem in enumerate(wordset) ])
    num_d = {}
    for word in d.keys():
        num_d[str(worddict[word])] = d[word]
    return num_d

def merge_dicts(d1, d2):
    d = d1.copy()
    d.update(d2)
    return d

def process_data(dataset):
    '''
    Call this one to do everything lol.
    '''
    if dataset == "shakespeare":
        lines = process_text(DATA_FILE)
        DEST = "data"
    if dataset == "spenspear":
        lines = process_text(DATA_FILE)
        lines.extend(process_text(SPENSER_FILE))
        DEST = os.path.join("data", "spenspear")
    if dataset == "beemovie":
        process_bee_text(BEE_RAW_FILE)
        lines = process_text(BEE_FILE)
        DEST = os.path.join("data", "bee")
    else:
        print "dataset " + dataset  + " not found"
        sys.exit()

    # tokenize
    tokenized_lines, wordset, st_words, punctuation, worddict = tokenize(lines)
    write_data(os.path.join(DEST, ST_FILE), st_words)   # save st words
    write_data(os.path.join(DEST, WORD_LIST_JSON), list(wordset))   
    write_data(os.path.join(DEST, TOKENIZED_WORDS), tokenized_lines)
    write_data(os.path.join(DEST, ENDLINE_PUNCTUATION), punctuation)
    write_data(os.path.join(DEST, NUM_TO_WORD_DICT), worddict)      

    # Find parts of speech
    tokpos_words, tokpos_pos = pos_tokenize(tokenized_lines)
    write_data(os.path.join(DEST, TOKPOS_WORDS), tokpos_words)
    write_data(os.path.join(DEST, TOKPOS_POS), tokpos_pos)
    
    # reverse every line and convert to numbers
    tokenized_lines = [line[::-1] for line in tokenized_lines]
    num_tokenized_lines = word_to_num(tokenized_lines, wordset)
    write_data(os.path.join(DEST, REVERSE_NUM_TOKENIZED), num_tokenized_lines)

    # rhyme
    # poems = process_text_by_poem(DATA_FILE)
    # rhyme_pairs = get_rhyme_pairs(poems)
    # num_rhyme_pairs = word_to_num(rhyme_pairs, wordset)
    # write_data(os.path.join(DEST, RHYME_PAIRS_NUM), num_rhyme_pairs)


    # jank rhymes for bees
    rhyme_pairs = get_rhyme_pairs_bee(DEST, wordset)
    num_rhyme_pairs = word_to_num(rhyme_pairs, wordset)
    write_data(os.path.join(DEST, RHYME_PAIRS_NUM), num_rhyme_pairs)


    ## stress
    ## DO NOT TOUCH. DO NOT UNCOMMENT. THE GENERATED FILE IS BEING MANUALLY
    ## CHANGED.
    # stress_dict, nonwords = create_stress_dict(tokenized_lines)
    # num_stress_dict = word_to_num_dict(stress_dict, wordset)
    # write_data(os.path.join(DEST, STRESS_DICT), num_stress_dict)
    # write_data(os.path.join(DEST, NONWORD), nonwords)


# This main is for testing purposes only
def main():
    # dataset = "shakespeare"
    # dataset = "spenspear"
    dataset = "beemovie"

    process_data(dataset)

    # lines = process_text(DATA_FILE)
    # tokenized_lines, wordset, st_words, punctuation, worddict = tokenize(lines)
    # tokenized_lines = [line[::-1] for line in tokenized_lines]
    # num_tokenized_lines = word_to_num(tokenized_lines, wordset)

    # nonwords = read_data('data/nonword_stress.json')
    # nonwords_dict = word_to_num_dict(nonwords, wordset)
    # write_data('nonword_stress.json', nonwords_dict)

    
    ## FIX THE STRESS DICT
    # stress_dict = read_data(os.path.join("data","spenspear",STRESS_DICT))
    # makemedict = {}
    # for s in stress_dict:
    #     makemedict[str(s[0])] = s[1]
    # print makemedict
    # write_data(os.path.join("data","spenspear",STRESS_DICT), makemedict)


if __name__ == "__main__":
    main()

    # stress_dict = read_data('data/stress_dict.json')
    # stress_dict_2 = read_data('data/spenspear/stress_dict.json')
    # merged_dict = merge_dicts(stress_dict, stress_dict_2)
    # write_data('stress_dict.json', merged_dict)
    
    # nonwords = read_data('nonword_stress_spen_num.json')
    # stress_dict = read_data('data/spenspear/stress_dict_comb.json')
    # d = merge_dicts(nonwords, stress_dict)
    # write_data('nonword_stress_comb.json', d)


