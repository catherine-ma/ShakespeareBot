'''
CS155 ShakespeareBot
postprocessing.py
'''

import re
import csv
import random
import json 
import string
import os

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

DATA_FILE = os.path.join("data", "shakespeare.txt")
SPENSER_FILE = os.path.join("data", "spenser.txt")


'''
Read and write to a file ezpz.
'''
def write_word_list(dest, words):
    with open(dest, 'w') as f:
        wr = csv.writer(f, delimiter=',', quotechar='"')
        wr.writerow(list(words))
        f.close()
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

def reintroduce_st(str, DEST):
    '''
    Reintroduce the "'st" on the end of the words which could use it.
    '''
    st_words = read_data(os.path.join(DEST, ST_FILE))
    for word in st_words:
        while True:
            worind = str.find(word)
            if worind == -1:
                break
            nxtchar = str[worind + len(word)]
            if word == "fleet":
                print nxtchar
            if worind + len(word) >= len(str) or (not nxtchar.isalpha() and nxtchar != "'"):
                str = str.replace(word, word + "'st", 1)
            else:
                break
    return str


def get_end_punc(DEST):
    '''
    Returns a random punctuation mark for the end of a line. The distribution
    of punctuation returned is proportional the Shakespearean sonnets.

    Since some lines do not have ending punctuation, this function also returns
    the empty string.
    '''
    punctuation = read_data(os.path.join(DEST, ENDLINE_PUNCTUATION))
    count = random.random() * punctuation['linecount']
    for k, v in punctuation['punc'].iteritems():
        count -= v
        if count < 0:
            return k
    return ""


def fix_hyphens(str):
    return str.replace(" - ", "-")


def fix_punctuation(str):
    '''
    Fixes punctuation.
    - Deletes punctuation at the beginning of the line.
    - Double spaces.
    - Corrects punctuation with random spaces around it.
    - Two punctuation in a row.
    '''
    # remove punctuation at beginning of line
    misc_beginning_punctuation = ["'s"]
    if str.strip()[0] in string.punctuation or \
       str.strip()[0] in misc_beginning_punctuation:
        str = str.strip()[1:]
    
    # remove multiple spaces in a row
    str = ' '.join(str.split())

    # miscellaneous replacements
    str = str.replace(" i ", " I ")
    str = str.replace(",s", "'s")
    
    # remove spaces before punctuation if appropriate
    remove_space_punctuation = ["!", ",", ".", ";", ":", "?", "'s"]
    for punc in remove_space_punctuation:
        str = str.replace(" " + punc, punc)

    # remove punctuation entirely if appropriate
    remove_punctuation = ["(", ")", "'"]
    for punc in remove_punctuation:
        str = str.replace(" " + punc + " ", " ")
    
    # two punctuation in a row
    punctuation = ["!", "'", ",", ".", ";", ":", "?", "'s", "-"]
    newstr = ""
    found = False
    for c in str:
        if c in punctuation:
            if found:
                continue
            else:
                found = True
        else:
            found = False
        newstr += c
    str = newstr
    return str


def post_process_line(str, DEST):
    str = fix_hyphens(str)
    str = reintroduce_st(str, DEST)
    str = fix_punctuation(str)
    return str



# This main function is for testing purposes only
def main():
    sonnet = "feed forget . feel frown fleet   !fun fudge fuck fawn fanta four fourth fleeting,,"
    # reintroduce_st(sonnet)
    # print get_end_punc()
    print post_process_line(sonnet)

if __name__ == "__main__":
    main()
