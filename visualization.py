import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from preprocessing import read_word_list

## Top ten words of each state. 
def topWords(O, words, n=10):
    N = len(O)
    words = np.asarray(words)
    topWords = [0 for i in range(N)]
    for state in range(N):
        prob = np.asarray(O[state])
        topInd = prob.argsort()[-n:][::-1]
        topWords[state] = words[topInd]
    return np.asarray(topWords)

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