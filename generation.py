import csv
import json
import numpy as np
import postprocessing as pp
import random
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


def read_data(dest):
    with open(dest, 'r') as f:
        return json.load(f)
    
def read_matrix(dest):
    with open(dest, 'r') as f:
        rd = csv.reader(f, delimiter=',', quotechar='"')
        return [[float(i) for i in row] 
                for row in rd]

## Grab Hmm matrixes A and O from stored files. 
def get_HMM(name):
    path_a = os.path.join("models", name + '_A.csv')
    path_o = os.path.join("models", name + '_O.csv')
    A = read_matrix(path_a)
    O = read_matrix(path_o)
    return A, O

## Prime the ends of sonnets by generating rhyming pairs only and returning
## 1-word lines. 
def prime_sonnet(DEST):
    poem = [[] for i in range(14)]
    rhyme_pairs = read_data(os.path.join(DEST, RHYME_PAIRS_NUM))
        
    # Generate 7 rhyming word pairs and put them into the poem
    for n in range(7):
        
        # Sample rhyming pairs with uniform distribution. 
        rand_ind = random.randrange(len(rhyme_pairs))
        rhyme_word1, rhyme_word2 = rhyme_pairs[rand_ind]
        a = [rhyme_word1]
        b = [rhyme_word2]
        
        # Place them in current place in poem
        if n == 0 or n == 1:
            poem[n] = a
            poem[n+2] = b
        elif n == 2 or n == 4:
            poem[2*n] = a
            poem[2*n+2] = b
        elif n == 3 or n == 5:
            poem[2*n-1] = a
            poem[2*n+1] = b
        if n == 6:
            poem[12] = a
            poem[13] = b    
    return poem


## Poem generated is a list of lists of integers. Each list contains a line of
## indexes representing words, backward. 
def generate_sonnet(A, O, DEST):
    n_states = len(A) 
    n_words = len(O[0])
    poem = prime_sonnet(DEST)
    stress_dict = read_data(os.path.join(DEST, STRESS_DICT))
    encoding = read_data(os.path.join(DEST, WORD_LIST_JSON))
    
    # Fill in the rest of the line
    O = np.asarray(O)
    for i in range(14):
        
        # Keep track of number of syllables and currently ending stress
        # Stress is 1 for stressed, 0 for relaxed
        start_word = poem[i][0]
        if str(start_word) not in stress_dict:
            print "stress not in dict", start_word
            start_stress = [1]
            syllables = 1
        else:
            start_stress = stress_dict[str(start_word)]
            syllables = len(start_stress)
            if syllables == 0:
                stress = -1
            else:
                stress = start_stress[0]
        
        
        # Find the starting state using our rhyming word
        state_probs = O[:,start_word]
        prob_sum = sum(state_probs)
        state_probs = [m / prob_sum for m in state_probs]
        ys = [int(np.random.choice(n_states, p=state_probs))]
        
        # Iterate until each line reaches 10 syllables
        while syllables < 10:
            y = ys[-1]
            while True:
                cand = int(np.random.choice(n_words, p=O[y]))            
                if str(cand) not in stress_dict:
                    cand_stress = [1]
                    print "stress not in dict", encoding[cand]
                else:
                    print "yay"
                    cand_stress = stress_dict[str(cand)]
                cand_n_syl = len(cand_stress)
                
                # If the word is punctuation
                if cand_n_syl == 0:
                    cand_end_stress = -1
                    cand_start_stress = -1
                else:
                    cand_end_stress = cand_stress[-1]
                    cand_start_stress = cand_stress[0]
                
                # If the word doesn't satisfy syllable and stress conditions
                if syllables + cand_n_syl > 10:
                    continue
                if cand_n_syl != 1 and cand_end_stress == stress:
                    continue
                break                
            
            stress = cand_stress[0]
            syllables += cand_n_syl
            poem[i].append(cand)
            ys.append(int(np.random.choice(n_states, p=A[y])))
            
    return poem

## Decodes each line of a poem of integers. Returns a list of strings with the
## lines of the poem
def decode_sonnet(code, DEST):
    n_lines = len(code)
    poem = ['' for i in range(n_lines)]
    encoding = read_data(os.path.join(DEST, WORD_LIST_JSON))
    for i in range(n_lines):
        n_words = len(code[i])
        words = []
        
        # Decipher the words backward
        for j in range(n_words-1, -1, -1):
            words.append(encoding[code[i][j]])
        line = str(' '.join(words).capitalize())
        line = pp.post_process_line(line, DEST)
        # line = pp.fix_punctuation(line)
        if i != n_lines - 1:
            line += pp.get_end_punc(DEST)
        else:
            line += '.'
        poem[i] = str(line)
    
    return poem
            
## Get number of syllables. If not available, return 1 and print an error 
## message.
def numSyl(stress_dict, word):
    if word in stress_dict:
        return len(stress_dict[word])
    print word, "not found in stress_dict"
    return 1

## Generate poem in the style of a haiku. Returns a list of strings containing
## the lines
def generate_haiku(A, O, DEST):
    stress_dict = read_data(os.path.join(DEST, STRESS_DICT))
    n_states = len(A)
    n_words = len(O[0])
    poem = [0 for i in range(3)]
    for i in range(3):
        if i == 1:
            tot_syl = 7
        else:
            tot_syl = 5

        start_word = random.randrange(n_words)
        syl  = numSyl(stress_dict, word)
        poem[i] = [start_word]
        
        while syl < tot_syl:
            cand = int(np.random.choice(n_words, p=O[y])) 
        
    return poem

## Write poem stored in lines, which has one line per row into file prefixed
## by name. 
def write_poem(lines, name):
    dest = os.path.join("poems", name + ".txt")
    with open(dest, 'w') as f:
        for line in lines:
            f.write(line + '\n')

def main():
    use_spenser = True
    DEST = "data"
    if use_spenser:
        DEST = os.path.join("data","spenspear")

    # A, O = get_HMM('spenspear_10_states')
    A, O = get_HMM('spenspear_12_states')
    code = generate_sonnet(A, O, DEST)
    print code
    #code = [[1, 2], [3, 4]]
    poem = decode_sonnet(code, DEST)
    print poem
    write_poem(poem, 'test')
    #write_poem(poem, 'shakespeare_state6_it1000')
    
main()