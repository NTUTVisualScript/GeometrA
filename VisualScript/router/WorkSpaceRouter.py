from flask import request, jsonify
from tkinter import filedialog, Tk

from VisualScript import app
from VisualScript.src import WORKSPACE as ws
from VisualScript.src.File.FileManager import *

@app.route('/VisualScript/WorkSpace')
def getWorkSpace():
    return jsonify(ws.getTreeJSON())

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

def checkName(path, name, n=0):
    print(os.listdir(path))
    print(n)
    if n != 0:
        fName = name + '(' + str(n) + ')'
    else:
        fName = name
    print(fName)
    if fName in os.listdir(path):
        return checkName(path, name, n = n + 1)
    return n

@app.route('/VisualScript/WorkSpace/addSuite', methods=['POST'])
def addSuite():
    project = request.form['Project']
    suite = 'New Suite'
    n = checkName(ws.projects[project].path, suite)
    if n != 0:
        suite = suite + '(' + str(n) + ')'

    ws.projects[project].add(suite)
    return suite

@app.route('/VisualScript/WorkSpace/addCase', methods=['POST'])
def addCase():
    project = request.form['Project']
    suite = request.form['Suite']
    case = 'New Case'
    n = checkName(ws.projects[project].suites[suite].path, case)
    if n != 0:
        case = case + '(' + str(n) + ')'
    ws.projects[project].add(suite, case)
    return case

@app.route('/VisualScript/WorkSpace/delete', methods=['POST'])
def deleteFile():
    if 'Case' in request.form:
        case = request.form['Case']
        suite = request.form['Suite']
        project = request.form['Project']
        ws.projects[project].suites[suite].delete(case)
    elif 'Suite' in request.form:
        suite = request.form['Suite']
        project = request.form['Project']
        ws.projects[project].delete(suite)
    else:
        project = request.form['Project']
        ws.delete(project)

    return ""

@app.route('/VisualScript/WorkSpace/rename', methods=['POST'])
def rename():
    new = request.form['new']
    try:
        if 'Case' in request.form:
            case = request.form['Case']
            suite = request.form['Suite']
            project = request.form['Project']
            if case == new:
                return ''
            ws.projects[project].suites[suite].rename(case, new)
        elif 'Suite' in request.form:
            suite = request.form['Suite']
            project = request.form['Project']
            if suite == new:
                return ''
            ws.projects[project].rename(suite, new)
        else:
            project = request.form['Project']
            if project == new:
                return ''
            ws.rename(project, new)
        return ''
    except Exception as e:
        return new

@app.route('/VisualScript/WorkSpace/save', methods=['POST'])
def save():
    xml = request.form['xml']
    code = request.form['code']
    ws.save(xml, code)
    return 'success'

@app.route('/VisualScript/WorkSpace/open', methods=['POST'])
def open():
    focus = request.form
    ws.setFocus(focus)
    xml = ws.open()
    return xml
