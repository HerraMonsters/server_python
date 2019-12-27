import sys
import re
import pandas as pd
import json
from underthesea import sent_tokenize
from underthesea import pos_tag
from underthesea import word_tokenize
from textblob import TextBlob
import datetime
from datetime import timezone
import time
import datetime



#thiết lập thư viện stopword tiếng Việt
vnStopword = []
f = open("stopwords.txt", encoding='utf-8')
for x in f:
  x = re.sub(r'[\n]', '',x)
  vnStopword.append(x)

#thiết lập dictionary cho numberSeeker
with open('numberSeeker.json', 'r', encoding="utf-8") as k:
  numjson = k.read()
numjson = re.sub(r'[\n]','',numjson)
numData = json.loads(numjson)

#thiết lập dictionary cho vnAbbriviate
with open('vnabb.json','r', encoding="utf-8") as j:
  abbjson = j.read()
abbjson = re.sub(r'[\n]','',abbjson)
vnAbbriviate = json.loads(abbjson)

def standardize(defmss,switch): #hàm xử lý ban đầu
  if not defmss:
    return('')
  else:
    defmss = defmss.lower()
    mss=defmss
    if switch == 0: #0 cho trường date
      mss = re.sub(r'[^\w\s/]', ' ',defmss) #lược dấu
      mss = re.sub(r'[/]', ' / ',mss)
      mss = word_tokenize(mss) #tokenize, rawmss theo kiểu array
    if switch == 1: #1 cho trường pickupAddress, takeoffAddress; biến feedback
      mss = re.sub(r'[^\w\s]', ' ',defmss)
      mss = word_tokenize(mss)
    if switch == 2: #2 cho trường time
      mss = re.sub(r'[^\w\s]', ' ',defmss)
      mss = re.sub(r'[h]', ' h ',mss)
      mss = word_tokenize(mss)
    return mss

def sw_remover(stdmss): #hàm lược stopword
  if not stdmss:
    return('')
  else:
    mss = ''
    for x in stdmss:
      if x not in vnStopword:
        mss = mss + x + ' '
    return mss

def numSeeker(finalmss): #lọc dữ liệu số cho date và seats
  allNum = []
  finalmss = word_tokenize(finalmss)
  for i,x in enumerate(finalmss):
    if x.isdigit():
      allNum.append(x)
    #if x == '/':
      #allNum.append(int(finalmss[i+1]))
      #i=i+3
    #if x == 'tháng':
      #allNum.append(int(finalmss[i+1]))
      #i=i+3
  return allNum

def timeSeeker(finalmss): #chuẩn hóa thời gian
  time = [0,0,0]
  index = 0
  finalmss = word_tokenize(finalmss)
  for i,x in enumerate(finalmss):
    if x.isdigit():
      if time[index] == 0:
        time[index] = int(x)
      else:
        index+=1
        time[index] = int(x)
    else:
      if x == 'rưỡi':
        time[1]=30
        time[2]=00
      if x == 'kém':
        time[1]=60-int(finalmss[i+1])
        time[2]=00
        break
  return time


def placecorrect(finalmss): #chuẩn hóa dữ liệu địa điẻm
  place = ''
  for x in finalmss:
    place = place + x + ' '
  return place.strip()


#Bỏ stop word và chuẩn hóa
def pre_processing(str, switch):
	return sw_remover(standardize(str, switch))

def getTime(data): #Chuẩn hóa thời gian
  year = datetime.date.today().year
  time = [year]
  for i in numSeeker(pre_processing(data['date'], 0)): 
    time.append(i)
  for j in timeSeeker(pre_processing(data['time'],2)):
    time.append(j)

  d = datetime.datetime(int(time[0]),int(time[1]),int(time[2]),int(time[3]),int(time[4]),int(time[5]))
  return d.replace(tzinfo=timezone.utc).timestamp()


### HÀM XỬ LÝ PHẢN ÁNH ###
def abbriviateCorrect(mss): #xử lý viết tắt
  final = ''
  for i,x in enumerate(mss):
    if x in vnAbbriviate:
      final = final + vnAbbriviate[x] + ' '
    else:
      final = final + x +  ' '
  return final.strip()
### KẾT THÚC HÀM XỬ LÝ PHẢN ÁNH ###


#hàm trả kết quả của tiền xử lý
def return_result(data):
	status = int(data['status'])
	arr = data['data']
	
	request = {}
	if status == 0:
		#lấy ghế ngồi
		seats = numSeeker(pre_processing(arr['seats'],2))
		request = {
			"status":status,
			"data": {
				"pickupAddress":placecorrect(word_tokenize(pre_processing(arr['pickupAddress'],1))),
        "takeoffAddress":placecorrect(word_tokenize(pre_processing(arr['takeoffAddress'],1))),
        "startTime": getTime(arr),
        "seats": seats[0]
			}
		}
	else:
		request = {
			"status": status,
			"data": abbriviateCorrect((standardize(arr,1)))
		}
	return request


#Hàm xử lý
# def book_car(data):
#     pickupAddress = data["pickupAddress"]
#     takeoffAddress = data["takeoffAddress"]
#     time = data["startTime"]
#     seats = data["seats"]
#     print(pickupAddress)
#     print(takeoffAddress)
#     print(time)
#     print(seats)
#     print("success")
#     return 

#hàm tạo từ điển cảm xúc
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

#hàm tách từ
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


#hàm phân tích cảm xúc
def evaluate(data):
    dictionary = dict()
    data = data.lower()
    words = text_tokenize(data)
    #print(words)
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
    if n_point > p_point:
      return {"message": 0}
    elif n_point < p_point:
      return {"message": 1}
    else:
      return {"message": 1000}