from flask import request, jsonify

from GeometrA import app
from GeometrA.src.Node import Node

from pprint import pprint
@app.route('/GeometrA/Node')
def getNode():
    n = Node()
    n.export()
    pprint(n.data())
    print(len(n.data()))
    return jsonify(n.data())
