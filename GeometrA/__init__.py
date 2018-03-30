from flask import Flask, request, render_template
from flask_cors import CORS

import os
import json

from GeometrA.src import WORKSPACE as ws
from GeometrA.src.Record import *

app = Flask(__name__)
CORS(app)

@app.route('/GeometrA')
def html():
    return render_template('index.html')

@app.route('/GeometrA/checkLog')
def checkLog():
    if os.path.isfile('./record.log'):
        return 'exist'
    return 'not exist'

@app.route('/GeometrA/saveLog')
def saveLog():
    try:
        exportLog()
        return 'Success'
    except Exception as e:
        return 'Fail'

@app.route('/GeometrA/log')
def log():
    try:
        loadLog()
        return 'Success'
    except Exception as e:
        print(e)
        return 'Fail'

from GeometrA.router import WorkSpaceRouter
from GeometrA.router import TestScriptRouter
