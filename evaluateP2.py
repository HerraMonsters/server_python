import re
from create_dictP2 import dict
from text_tokenizeP2 import text_tokenize

def evaluate(data):
    dictionary = dict()
    data = data.lower()
    words = text_tokenize(data)
    print(words)
    pos_point = []
    neg_point = []
    ww = []
    for word in words:
        for w in dictionary:
            for i, val in enumerate(w):
                if i == 2:
                    if word in w[2]:
                        ww.append(word)
                        pos_point.append(w[0])
                        neg_point.append(w[1])
    print(ww, "\n", pos_point, "\n", neg_point)
    n_point = 0
    p_point = 0
    for p in neg_point:
        n_point += float(p)
    for p in pos_point:
        p_point += float(p)
    print("positive point:",p_point, "\n","negative point:", n_point)
    return p_point, n_point