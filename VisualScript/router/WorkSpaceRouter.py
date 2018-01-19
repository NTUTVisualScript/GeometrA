from flask import request, jsonify
from tkinter import filedialog, Tk

from VisualScript import app
from VisualScript.src import WORKSPACE
from VisualScript.src.File.FileManager import *
from VisualScript.src.File.WorkSpace import WorkSpace

@app.route('/VisualScript/WorkSpace')
def getWorkSpace():
    return jsonify(WORKSPACE.getTreeJSON())

@app.route('/VisualScript/WorkSpace/create', methods=['POST'])
def createProject():
    if ('projectName' not in request.form) or ('suiteName' not in request.form) or \
        ('caseName' not in request.form) or ('projectPath' not in request.form):
        return "Failed"
    info = {
        'project' : request.form['projectName'],
        'suite' : request.form['suiteName'],
        'case' : request.form['caseName'],
        'path' : request.form['projectPath']
    }
    try:
        new(info)
        path = info['path']
        jsonPath = path + '/' + info['project'] + '/' + info['project'] + '.json'
        load(jsonPath)
        return "Success"
    except Exception as e:
        print(e)
        return "Failed"

@app.route('/VisualScript/WorkSpace/load', methods=['POST'])
def loadProjects():
    if 'projectPath' not in request.form:
        return "Failed"
    path = request.form['projectPath']
    try:
        load(path)
        return "Success"
    except Exception as e:
        print(e)
        return "Failed"


@app.route('/VisualScript/WorkSpace/getFilePath')
def getFilePath():
    root = Tk()
    f = filedialog.askopenfile(title="Select File", filetypes=[("TestCase JSON Files", "*.json")])
    root.destroy()
    filePath = f.name
    return filePath

@app.route('/VisualScript/WorkSpace/getProjectPath')
def getProjectPath():
    root = Tk()
    projectPath = filedialog.askdirectory()
    root.destroy()
    return projectPath
