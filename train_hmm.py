from HMM import unsupervised_HMM


## Trains an unsupervised HMM on data X using n_states. The resulting 
## transition and emission matrices will be saved in two files, with the name
## prefix specified. 
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
    
    # Save the transition matrix into file
    fname_A = "models\\" + name + "_A.txt"
    with open(fname_A, "w") as fle:
        for r in HMM.A:
            fle.write(r)
    
    # Save the observation matrix in file
    fname_O = "models\\" + name + "_O.txt"
    with open(fname_O, "w") as fle:
        for r in HMM.O:
            fle.write(r)