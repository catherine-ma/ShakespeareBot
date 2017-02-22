import numpy as np

def topWords(O, words, n=10):
    N = len(O)
    words = np.asarray(words)
    topWords = [0 for i in range(N)]
    for state in range(N):
        prob = np.asarray(O[state])
        topInd = prob.argsort()[-n:][::-1]
        topWords[state] = words[topInd]
    return np.asarray(topWords)

def 