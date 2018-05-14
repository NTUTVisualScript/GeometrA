from flask import request, jsonify

from GeometrA import app
from GeometrA.src.Node import Node

@app.route('/GeometrA/Node')
def getNode():
    n = Node()
    n.export()
    return jsonify(n.data())
