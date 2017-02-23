import csv
import json
import postprocessing

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
    path_a = 'models\\' + name + '_A.csv'
    path_o = 'models\\' + name + '_O.csv'
    A = read_matrix(path_a)
    O = read_matrix(path_o)
    return A, O

## Poem generated is a list of lists of integers. Each list contains a line of
## indexes representing words, backward. 
def generate_sonnet(A, O):
    poem = [[] for i in range(14)]
    rhyme_pairs = read_data('data\\rhyme_pairs.json')
    
    # Generate 7 rhyming lines
    for n in range(7):
        line1 = []
        line2 = []
        
        
        
        # Place them in current place in poem
        if n == 6:
            poem[12] = line1
            poem[13] = line2
        else:
            poem[n]   = line1
            poem[n+2] = line2
            
    return poem

## Decodes each line of a poem of integers. Returns a list of strings with the
## lines of the poem
def decode_sonnet(code, encoding_dest):
    n_lines = len(code)
    poem = ['' for i in range(n_lines)]
    encoding = read_data(encoding_dest)
    for i in range(n_lines):
        n_words = len(code[i])
        words = []
        
        # Decipher the words backward
        for j in range(n_words-1, -1, -1):
            words.append(encoding[code[i][j]])
        line = str(' '.join(words))
        line = line.capitalize()
        poem[i] = line
    poem[-1] += '.'
    
    return poem
            
            

## Generate poem in the style of a haiku. Returns a list of strings containing
## the lines
def generate_haiku(A, O):
    poem = []
    
    return poem

## Write poem stored in lines, which has one line per row into file prefixed
## by name. 
def write_poem(lines, name):
    dest = 'poems\\' + name + '.txt'
    with open(dest, 'w') as f:
        for line in lines:
            f.write(line + '\n')

def main():
    A, O = get_HMM('shakespeare_6_states')
    #code = generate_sonnet(A, O)
    code = [[1, 2], [3, 4]]
    poem = decode_sonnet(code, 'data\\words.json')
    write_poem(poem, 'test')
    #write_poem(poem, 'shakespeare_state6_it1000')
    
main()