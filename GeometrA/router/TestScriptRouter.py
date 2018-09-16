from flask import request, jsonify

from GeometrA import app
from GeometrA.src import WORKSPACE as ws
from GeometrA.src.TestScript import TestScript

@app.route('/GeometrA/TestScript/run', methods=['POST'])
def run():
    caseList = request.form['cases'].split(',')
    print(caseList)
    ts = TestScript()
    for case in caseList:
        caseRoute = case.split('/')
        path = ws.projects[caseRoute[0]].suites[caseRoute[1]].path + '/' +caseRoute[2]
        ts.load(path)
    return ts.runAll()
