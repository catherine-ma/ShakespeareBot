import csv
import numpy as np
import networkx as nx
import os

import generation as gn

def main():
    A, O = gn.get_HMM('spenspear_10_states')
    encoding = gn.read_data(os.path.join("data", "spenspear", gn.WORD_LIST_JSON))
    for t in topWords(O, encoding, 'spenspear_10_states'):
        print t

## Top ten words of each state. 
def topWords(O, words, name, n=10):
    N = len(O)
    words = np.asarray(words)
    topWords = [0 for i in range(N)]
    for state in range(N):
        prob = np.asarray(O[state])
        topInd = prob.argsort()[-n:][::-1]
        topWords[state] = words[topInd]
        
    # Format it like a table
    table = [[0 for i in range(N)] for j in range(11)]
    for i in range(N):
        table[0][i] = 'State ' + str(i+1)
    for j in range(1, 11):
        for i in range(N):
            table[j][i] = topWords[i][j-1]
    
    # Write to csv 
    fname = os.path.join('visualization', 'top_ten_' + name + '.csv')
    with open(fname, 'w') as f:
        wr = csv.writer(f, delimiter=',', quotechar='"', lineterminator='\n')
        for r in table:
            wr.writerow(r)    
    
    return table

## Probability of words of each part of speech in each state. Returns array of 
## dictionaries. Outer array index refers to state number. Dictionary has parts
## of speech as keys and sums of probabilities as values. 
def statePartsOfSpeech(O, PoS):
    N = len(O) 
    allProbs = [{} for i in range(N)]
    for state in range(N):
        probs = allProbs[state]
        for word in range(len(O[state])):
            pos = PoS[word]
            if pos in probs:
                probs[pos] += O[state][word]
            else:
                probs[pos] = O[state][word]
    return allProbs

#Ot = [[.7, .4, .5], [.3, .6, .8]]
#wordst = ['a', 'b', 'c']
#PoSt = ['NN', 'NN', 'V']
#print statePartsOfSpeech(Ot, PoSt)

def stateNumWords(O):
    pass

"""
## Draw Markov diagram. 
def graphHMM(A):
    n_states = len(A) 
    
    # Construct graph 
    G = nx.DiGraph()
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos,
                           nodelist = range(n_states),
                           node_color = 'b',
                           node_size = 2000,
                           alpha = 0.5)
    for i in range(n_states):
        for j in range(n_states):
            G.add_edge(i, j, weight = A[i][j])
    nx.draw(G)
    plt.show()

At = [[.7, .4, .5], [.3, .6, .8], [.5, .6, .7]]
graphHMM(At)
"""

main()