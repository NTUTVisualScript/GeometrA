from flask import Flask, request, render_template, jsonify
from VisualScript import app

from VisualScript.src.main import WORKSPACE
from VisualScript.src.File.FileManager import *

class WorkSpaceRouter():
    def html(self):
        return render_template('index.html')


    def createProject(self, info):
        try:
            new(info)
            path = info['path']
            jsonPath = path + '/' + info['project'] + '/' + info['project'] + '.json'
            return load(jsonPath)
        except:
            return False

    def getWorkSpace(self):
        return jsonify(WORKSPACE.getTreeJSON())

wsr = WorkSpaceRouter()

@app.route('/VisualScript')
def html():
    return wsr.html()

@app.route('/VisualScript/create', methods=['POST'])
def createProject():
    req = {
        'project' : request.form['project'],
        'suite' : request.form['suite'],
        'case' : request.form['case'],
        'path' : request.form['path']
    }
    return wsr.createProject(req)

@app.route('/VisualScript/getWorkSpace')
def getWorkSpace():
    return wsr.getWorkSpace()
