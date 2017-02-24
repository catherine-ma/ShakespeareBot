import csv
import numpy as np
import networkx as nx
import operator
import os

import generation as gn

def main():
    A, O = gn.get_HMM('spenspear_10_states')
    encoding = gn.read_data(os.path.join("data", "spenspear", gn.WORD_LIST_JSON))
    pos_dict = gn.read_data(os.path.join("data", "spenspear", gn.TOKPOS_DICT))
    statePOS(O, pos_dict)
    

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
def statePOS(O, PoS):
    N = len(O) 
    
    # Find probabilities for all parts of speech
    allProbs = [{'PUNC' : 0.0} for i in range(N)]
    for state in range(N):
        probs = allProbs[state]
        for word in range(len(O[state])):
            pos = str(PoS[str(word)])
            if not pos.isalpha():
                probs['PUNC'] += O[state][word]
                continue
            if pos in probs:
                probs[pos] += O[state][word]
            else:
                probs[pos] = O[state][word]
                
    # Find just positive probabiliites
    posProbs = [{} for i in range(N)]
    for i in range(N):
        for key, value in allProbs[i].items():
            if value > 0:
                posProbs[i][key] = value
    
    # Get only the top 5 types 
    top5 = [0 for i in range(N)]
    for i in range(N):
        top5[i] = sorted(posProbs[i].items(), key=operator.itemgetter(1))[::-1][:5]
        
    # Find remaining probability
    remainProb = [1. for i in range(N)]
    for i in range(len(top5)):
        for perc in top5[i]:
            remainProb[i] -= perc[1]
    for i in range(len(remainProb)):
        print i+1, remainProb[i]
    
    for t in top5:
        print "STATE"
        for s in t:
            print s
        
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