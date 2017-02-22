import csv
from HMM import unsupervised_HMM


## Trains an unsupervised HMM on data X using n_states.
def train(X, n_states, name):
    HMM = unsupervised_HMM(genres, n_states)
    
    # Print the transition matrix
    print("Transition Matrix:")
    print('#' * 70)
    for i in range(len(HMM.A)):
        print(''.join("{:<12.3e}".format(HMM.A[i][j]) for j in range(len(HMM.A[i]))))
    print('')
    print('')
    
    # Print the observation matrix
    print("Observation Matrix:  ")
    print('#' * 70)
    for i in range(len(HMM.O)):
        print(''.join("{:<12.3e}".format(HMM.O[i][j]) for j in range(len(HMM.O[i]))))
    print('')
    print('')    
    
    # Write trained model to files
    writeModel(HMM.A, HMM.O, name)


## Write transition and emission matrices into two files, with the name
## prefix specified. 
def writeModel(A, O, name):    
    # Save the transition matrix into file
    fname_A = 'models\\' + name + '_A.csv'
    with open(fname_A, 'w') as f:
        wr = csv.writer(f, delimiter=',', quotechar='"', lineterminator='\n')
        for r in A:
            wr.writerow(r)
    
    # Save the observation matrix in file
    fname_O = 'models\\' + name + '_O.csv'
    with open(fname_O, 'w') as f:
        wr = csv.writer(f, delimiter=',', quotechar='"', lineterminator='\n')
        for r in O:
            wr.writerow(r)
            
Ot = [[.7, .4, .5], [.3, .6, .8]]
At = [[.7, .4, .5], [.3, .6, .8], [.5, .6, .7]]
writeModel(At, Ot, "test")