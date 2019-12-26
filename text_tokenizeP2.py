from underthesea import word_tokenize
from textblob import TextBlob

def text_tokenize(data):
    words = []
    words1 = word_tokenize(data)
    for w in words1:
        words.append(w)
    
    bigrams = TextBlob(data).ngrams(2)
    e = ""
    for i, v in enumerate(bigrams):
        for j, val in enumerate(bigrams[i]):
            e += bigrams[i][j]
            e += " "
        e = e.strip()
        if e not in words1:
            words.append(e)
            e = ""

    trigrams = TextBlob(data).ngrams(3)
    e = ""
    for i, v in enumerate(trigrams):
        for j, val in enumerate(trigrams[i]):
            e += trigrams[i][j]
            e += " "
        e = e.strip()
        if e not in words1:
            words.append(e)
            e = ""

    quadgrams = TextBlob(data).ngrams(4)
    e = ""
    for i, v in enumerate(quadgrams):
        for j, val in enumerate(quadgrams[i]):
            e += quadgrams[i][j]
            e += " "
        e = e.strip()
        if e not in words1:
            words.append(e)
            e = ""
    return words
