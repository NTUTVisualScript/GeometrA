from flask import Flask, request, render_template, jsonify
from VisualScript import app

from VisualScript.src.File.FileManager import *

@app.route('/VisualScript')
def html():
    return wsr.html()

@app.route('/VisualScript/create', methods=['POST'])
def createProject():
    info = {
        'project' : request.form['project'],
        'suite' : request.form['suite'],
        'case' : request.form['case'],
        'path' : request.form['path']
    }
    try:
        new(info)
        path = info['path']
        jsonPath = path + '/' + info['project'] + '/' + info['project'] + '.json'
        return load(jsonPath)
    except:
        return False

@app.route('/VisualScript/getWorkSpace')
def getWorkSpace():
    return jsonify(WORKSPACE.getTreeJSON())

@app.route('/VisualScript/load', methods=['POST'])
def loadProjects():
    path = request.form['path']
    return load(path)
