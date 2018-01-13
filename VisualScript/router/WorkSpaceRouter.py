from flask import Flask, request, render_template, jsonify
from VisualScript import app
from VisualScript.src.File.WorkSpace import WorkSpace
import json

from flask import Flask, request, render_template
from flask_cors import CORS

class WorkSpaceRouter():
    def html(self):
        return render_template('index.html')


    def createProject(self, info):
        self.creator.new(info)
        path = info['path']
        jsonPath = path + '/' + info['project'] + '/' + info['project'] + '.json'
        project = json.load(open(jsonPath))
        self.ws = WorkSpace(path, project)

    def getWorkSpace(self):
        return jsonify(self.ws.getTreeJSON())

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
    wsr.createProject(req)

@app.route('/VisualScript/getWorkSpace')
def getWorkSpace():
    return wsr.getWorkSpace()
