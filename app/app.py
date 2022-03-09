import json
import flask

from process_articles import all_articles
from flask import jsonify
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)

@app.route("/")
def get():
    res = jsonify(all_articles)
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000)