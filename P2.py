import re
import json
from textblob import TextBlob
from underthesea import word_tokenize

with open('request2.json', 'r', encoding="utf-8-sig") as myfile:
    dt=myfile.read()
data = json.loads(dt)

#Tạo từ điển
dictionary = []
f = open('VietSentiWordnet_ver1.0.txt','r', encoding="utf8")
tag = ["POS", "ID", "PosScore", "NegScore", "SynsetTerms", "Gloss"]
lines = f.readlines()
words_list = []
word = []
for line in lines:
    zipp = zip(tag, line.split('\t'))
    word_info = list(zipp)
    for info in word_info:
        if(info[0] == "SynsetTerms"):
            word.append(info[1])
        if(info[0] == "PosScore"):
            word.append(info[1])
        if(info[0] == "NegScore"):
            word.append(info[1])
    words_list.append(word)
    word = []
for wl in words_list:
    dict = []
    for i, val in enumerate(wl):
        if(i==0):
            dict.append(val)
        if(i==1):
            dict.append(val)
        if(i==2):
            q = wl[2]
            q = re.sub(r'\d', "", q)
            q = re.sub(r'_', " ", q)
            q = q.split('#')
            r = []
            for i, val in enumerate(q):
                if(val != ""):
                    val = val.strip()
                    r.append(val)
    dict.append(r)
    dictionary.append(dict)
    dict = []

#Chia từ
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

#phân tích cảm xúc
def evaluate(data):
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
        
#Đặt xe 
def book_car(data):
    pickupAddress = data["pickupAddress"]
    takeoffAddress = data["takeoffAddress"]
    time = data["time"]
    date = data["date"]
    seats = data["seats"]
    print(pickupAddress)
    print(takeoffAddress)
    print(time)
    print(date)
    print(seats)
    print("success")

def data_process(request):
    if(request["status"] == 0):
        return book_car(request["data"])
    else:
        return evaluate(request["data"])

data_process(data)