'''
CS155 ShakespeareBot
postprocessing.py
'''

import re
import csv

ST_FILE = "data/st_words.csv"

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


def reintroduce_st(str):
    '''
    Reintroduce the "'st" on the end of the words which could use it.
    '''
    st_words = read_word_list(ST_FILE)
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
    print str


def fix_hyphens(str):
    return str.replace(" - ", "-")


# This main function is for testing purposes only
def main():
    sonnet = "feed forget feel frown fleet fun fudge fuck fawn fanta four fourth fleeting"
    reintroduce_st(sonnet)

if __name__ == "__main__":
    main()
