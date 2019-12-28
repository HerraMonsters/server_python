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

#Thiết lập từ chỉ sắc thái
with open('sacThai.json','r', encoding="utf-8") as l:
  sacjson = l.read()
sacjson = re.sub(r'[\n]','',sacjson)
sacThai = json.loads(sacjson)

#Thiết lập negDict
negDict = []
f = open("negDict.txt", encoding='utf-8')
for x in f:
  x = re.sub(r'[\n]', '',x)
  negDict.append(x)

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
    return mss.strip()

def numSeeker(finalmss): #lọc dữ liệu số cho date và seats
  allNum = []
  switch = 0
  finalmss = word_tokenize(finalmss)
  for i,x in enumerate(finalmss):
    if x.isdigit():
      allNum.append(x)
    if x == 'tháng' and len(allNum)==0:
      switch=1
  if switch == 1:
    c=allNum[0]
    allNum[0] = allNum[1]
    allNum[1] = c
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
  list_time = numSeeker(pre_processing(data['date'], 0))
  print(list_time)
  # Thay thế năm nếu người dùng nhập năm
  for k in list_time:
    if int(k) >= year:
      year = int(k)
      list_time.remove(k)
  time = [year]
  print(list_time)
  for i in list_time: 
    time.append(i)
  for j in timeSeeker(pre_processing(data['time'],2)):
    time.append(j)
  # print(time)
  if len(time)==6:
    d = datetime.datetime(int(time[0]),int(time[2]),int(time[1]),int(time[3]),int(time[4]),int(time[5]))
  return d.timestamp()*1000


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
    words1 = [" "] + words1 + [" ", " ", " "]
    words2 = []
    for i, w in enumerate(words1):
      if i<len(words1)-2:
        a = words1[i-1]
        b = w
        c = words1[i+1]
        words2.append(a)
        words2.append(b)
        words2.append(c)
        words.append(words2)
        words2 = []
    print(words)
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
    for i, word in enumerate(words):
        for j, val in enumerate(word):
          if(j == 1):
            for w in dictionary:
              for k, value in enumerate(w):
                if k==2 and val in value:
                  ppoint = float(w[0])
                  npoint = float(w[1]) 
                  a = ""
                  if word[0] in sacThai or word[2] in sacThai:
                   
                    if word[0] in sacThai and ppoint > npoint:
                      ppoint = ppoint*float(sacThai[word[0]])
                      a += word[0] + " " + val
                    elif word[0] in sacThai and ppoint < npoint:
                      npoint = npoint*float(sacThai[word[0]])
                      a += word[0] + " " + val
                    if word[2] in sacThai and ppoint > npoint:
                      ppoint = ppoint*float(sacThai[word[2]])
                      if a == "":
                        a += val + " " + word[2]
                      else:
                        a += " " + word[2]
                    elif word[2] in sacThai and ppoint < npoint:
                      npoint = npoint*float(sacThai[word[2]])
                      if a == "":
                        a += val + " " + word[2]
                      else:
                        a += " " + word[2]
                  else:
                    a = val
                  if word[0] in negDict:
                    x = ppoint
                    ppoint = npoint
                    npoint = x
                    a = word[0] + " " + a
                  ww.append(a)
                  pos_point.append(ppoint)
                  neg_point.append(npoint)
    print(ww, "\n", pos_point, "\n", neg_point)
    n_point = 0
    p_point = 0
    for p in neg_point:
        n_point += p
    for p in pos_point:
        p_point += p
    leng = len(ww)
    point = 0
    if leng != 0:
      point = ((p_point - n_point)/leng)
    print("positive point:",p_point, "\n","negative point:", n_point, "\n", "sentiment point: ", point)
    return {
      "positive point": p_point,
      "negative point": n_point,
      "point": point
      }