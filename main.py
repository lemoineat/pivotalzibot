#!/usr/bin/env python3
#codinf:utf-8

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1025, ssl_context='adhoc', debug=False)
