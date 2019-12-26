import json
from all_functions import book_car, evaluate, return_result

#test data
with open('request2.json', 'r', encoding="utf-8-sig") as myfile:
    dt=myfile.read()
data = json.loads(dt)
#########


def data_process(request):
    dt = return_result(request)
    if(request["status"] == 0):
        return book_car(dt["data"])
    else:
        return evaluate(dt["data"])
