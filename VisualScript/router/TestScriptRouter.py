from flask import request, jsonify

from VisualScript import app
from VisualScript.src import WORKSPACE as ws
from VisualScript.src import TESTSCRIPT as ts
import pprint

@app.route('/VisualScript/TestScript/run', methods=['POST'])
def run():
    caseList = request.form['cases'].split('/')
    pprint.pprint(caseList)
    path = ws.projects[caseList[0]].suites[caseList[1]].path + '/' +caseList[2]
    ts.load(path)
    return ts.runAll()
