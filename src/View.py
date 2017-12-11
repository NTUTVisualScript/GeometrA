from src import app
from flask import Flask, request, render_template, jsonify
from src.File.WorkSpace import WorkSpace
import pprint
import json

@app.route('/VisualScript')
def html():
    return render_template('index.html')

@app.route('/VisualScript/getWorkSpace', methods=['POST'])
def workSpace():
    path = request.form['path']
    project = json.load(open(path + '/Project.json'))
    ws = WorkSpace(path, project)
    
    return jsonify(ws.getTreeJSON())
