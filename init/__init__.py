from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Api for chatbot</h1>'''

@app.route('/api/v1/p1', methods=['GET', 'POST'])
def pre_processing():
    if request.method == 'POST':
        #do something
        return jsonify({'message': 'POST'})
    return jsonify({'message': 'GET'}), 200

@app.route('/api/v1/p2', methods=['GET', 'POST'])
def processing():
    return 0

