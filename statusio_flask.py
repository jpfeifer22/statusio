#!/usr/bin/python3


from flask import Flask, jsonify
from flask import send_from_directory
from flask import send_file
from flask import url_for 
from flask import request 
from flask import make_response
from flask import current_app
from flask_cors import CORS

from datetime import timedelta
from functools import update_wrapper
from pymongo import MongoClient
import six

import json
import os
import sys
import time
import pprint

import statusio_backend

app = Flask(__name__)
CORS(app)

@app.route("/", methods = ['GET'])
def base():
    return '{ "message": "Found the base." }'

@app.route("/home", methods = ['GET'])
def home():
    return '{ "message": "Welcome home." }'

################ All Applications ################

@app.route("/statusio/applications", methods = ['GET'])
def get_applications():
    return (statusio.get_application_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
