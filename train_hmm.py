import csv
import json
from HMM import unsupervised_HMM
# from hmmlearn.hmm import GaussianHMM

def read_data(dest):
    with open(dest, 'r') as f:
        return json.load(f)

## Trains an unsupervised HMM on data X using n_states.
def train(X, n_states, name):
    
    # Fit model
    HMM = unsupervised_HMM(X, n_states, 1000)
    A = HMM.A
    O = HMM.O
    
    # Using hmm learn
    #HMM = GaussianHMM(n_components=n_states)
    #HMM.fit(X) 
    #A = HMM.transmat_
    #O = HMM.
    
    # Print the transition matrix
    print("Transition Matrix:")
    print('#' * 70)
    for i in range(len(A)):
        print(''.join("{:<12.3e}".format(A[i][j]) for j in range(len(A[i]))))
    print('')
    print('')
    
    # Print the observation matrix
    print("Observation Matrix:  ")
    print('#' * 70)
    for i in range(len(O)):
        print(''.join("{:<12.3e}".format(O[i][j]) for j in range(len(O[i]))))
    print('')
    print('')    
    
    # Write trained model to files
    writeModel(A, O, name)


## Write transition and emission matrices into two files, with the name
## prefix specified. 
def writeModel(A, O, name):    
    # Save the transition matrix into file
    fname_A = 'models/' + name + '_A.csv'
    with open(fname_A, 'w') as f:
        wr = csv.writer(f, delimiter=',', quotechar='"', lineterminator='\n')
        for r in A:
            wr.writerow(r)
    
    # Save the observation matrix in file
    fname_O = 'models/' + name + '_O.csv'
    with open(fname_O, 'w') as f:
        wr = csv.writer(f, delimiter=',', quotechar='"', lineterminator='\n')
        for r in O:
            wr.writerow(r)
            
#Ot = [[.7, .4, .5], [.3, .6, .8]]
#At = [[.7, .4, .5], [.3, .6, .8], [.5, .6, .7]]
#writeModel(At, Ot, "test")

def main():
    X = read_data('data/bee/reverse_num_tokenized.json')
    
    # Change the number of states and model name here before your run!!!!!!!
    train(X, 9, 'bee_9_states')

main()