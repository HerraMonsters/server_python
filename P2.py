import json
from bookcarP2 import book_car
from evaluateP2 import evaluate

#test data
with open('request2.json', 'r', encoding="utf-8-sig") as myfile:
    dt=myfile.read()
data = json.loads(dt)
#########


def data_process(request):
    if(request["status"] == 0):
        return book_car(request["data"])
    else:
        return evaluate(request["data"])

data_process(data)