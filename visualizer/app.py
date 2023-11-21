# app.py (Flask backend)

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
from flask import send_from_directory

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def send_report(path):
    return send_from_directory('templates', path)

def predict(text):

    return {
        'text': text,
        'marking': {
            0: {'desc': 'Description for the first word', 'prob': 0.9},
            2: {'desc': 'Description for the third word', 'prob': 0.5},
            3: {'desc': 'Description for the forth word', 'prob': 0.7},
        },
    }

@app.route('/perform_magic', methods=['POST'])
def perform_magic():
    data = request.json
    user_input = data.get('userInput')
    return jsonify(predict(user_input))

if __name__ == '__main__':
    app.run(debug=True)
