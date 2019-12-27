from flask import Flask, request, jsonify, make_response
from all_functions import  evaluate, return_result

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Api for chatbot</h1>'''

@app.route('/api/v1/p1', methods=['GET', 'POST'])
def data_processing():
    if request.method == 'POST':
        dt = return_result(request.get_json())
        if(dt["status"] == 0):
            return jsonify(dt['data']), 200
        else:
            return evaluate(dt["data"])
    return jsonify({'message': 'GET'}), 200

# @app.route('/api/v1/p2', methods=['GET', 'POST'])
# def processing():
#     return 0

