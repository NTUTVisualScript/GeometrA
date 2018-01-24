from flask import Flask, request, render_template
from flask_cors import CORS

import os
import json

from VisualScript.src import WORKSPACE as ws
from VisualScript.src.Record import *

app = Flask(__name__)
CORS(app)

@app.route('/VisualScript')
def html():
    return render_template('index.html')

@app.route('/VisualScript/checkLog')
def checkLog():
    if os.path.isfile('./record.log'):
        return 'exist'
    return 'not exist'

@app.route('/VisualScript/saveLog')
def saveLog():
    try:
        exportLog()
        return 'Success'
    except Exception as e:
        return 'Fail'

@app.route('/VisualScript/log')
def log():
    try:
        loadLog()
        return 'Success'
    except Exception as e:
        print(e)
        return 'Fail'

from VisualScript import main
from VisualScript.router import WorkSpaceRouter
