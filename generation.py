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

## Get rhyming pairs
def rhyming_pairs(dest):
    pass

## Poem generated is a list of strings.
def generate_sonnet(A, O):
    poem = []
    
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
    with open(dest, 'r') as f:
        for line in lines:
            f.write(line)

def main():
    print read_data('data\\rhymes.json')
    
main()