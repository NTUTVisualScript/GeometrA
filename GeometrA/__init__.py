from flask import Flask, request, render_template
from flask_cors import CORS

import os
import json
import platform

from GeometrA.src import WORKSPACE as ws
from GeometrA.src.Record import *

app = Flask(__name__)
CORS(app)


LOG_FILE_NAME = '.geometra.log'
if (platform.system() == 'Windows'):
    GEOMETRA_ROOT = os.environ['USERPROFILE'] + '\\.GeometrA\\'
else:
    GEOMETRA_ROOT = os.environ['HOME'] + '/.GeometrA/'

if (not os.path.isdir(GEOMETRA_ROOT)):
    if (os.path.isfile()):
        os.remove(GEOMETRA_ROOT)
    os.mkdir(GEOMETRA_ROOT)
RECORD_FILE = GEOMETRA_ROOT + LOG_FILE_NAME

@app.route('/')
def html():
    return "Hello"
    # return render_template('index.html')

@app.route('/GeometrA/checkLog')
def checkLog():
    if os.path.isfile(RECORD_FILE):
        return 'exist'
    return 'not exist'

@app.route('/GeometrA/saveLog')
def saveLog():
    try:
        exportLog(RECORD_FILE)
        return 'Success'
    except Exception as e:
        return 'Fail'

@app.route('/GeometrA/log')
def log():
    try:
        loadLog(RECORD_FILE)
        return 'Success'
    except Exception as e:
        print(e)
        return 'Fail'

from GeometrA.router import WorkSpaceRouter
from GeometrA.router import TestScriptRouter
from GeometrA.router import ScreenRouter
from GeometrA.router import NodeRouter
