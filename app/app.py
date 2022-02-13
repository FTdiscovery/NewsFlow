import json
import flask

from flask import jsonify
from flask import Flask

app = Flask(__name__)

FNAME = 'current.json'

@app.route("/")
def get():
    with open(FNAME) as f:
        lis = json.load(f)
    return jsonify(d)

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000)