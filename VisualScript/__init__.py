from flask import Flask, request, render_template
from flask_cors import CORS

import os

from VisualScript.src import WORKSPACE as ws

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
    wslog = ws.log()
    log = {
        'WorkSpace': wslog,
    }
    try:
        with open('./record.log', 'w') as f:
            f.write(str(log).replace("'", '"'))
        return 'Success'
    except Exception as e:
        print(e)
        return 'Fail'

from VisualScript.router import WorkSpaceRouter
