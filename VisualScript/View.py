
from flask import Flask, request, render_template, jsonify
from VisualScript import app
from VisualScript.src.File.WorkSpace import WorkSpace
import pprint
import json

from flask import Flask, request, render_template
from flask_cors import CORS


# @app.route('/')
# def test():
#     return render_template('index.html')

class View():
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

view = View()

@app.route('/VisualScript')
def html():
    return view.html()

@app.route('/VisualScript/create', methods=['POST'])
def createProject():
    req = {
        'project' : request.form['project'],
        'suite' : request.form['suite'],
        'case' : request.form['case'],
        'path' : request.form['path']
    }
    view.createProject(req)

@app.route('/VisualScript/getWorkSpace')
def getWorkSpace():
    return view.getWorkSpace()
