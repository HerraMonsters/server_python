import re

def dict():
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
    return dictionary