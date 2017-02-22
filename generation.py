import csv
import postprocessing

def read_matrix(dest):
    with open(dest, 'r') as f:
        rd = csv.reader(f, delimiter=',', quotechar='"')
        return [[float(i) for i in row] 
                for row in rd]

def getModel(name):
    path_a = 'models\\' + name + '_A.csv'
    path_o = 'models\\' + name + '_O.csv'
    A = read_matrix(path_a)
    O = read_matrix(path_o)
    return A, O
