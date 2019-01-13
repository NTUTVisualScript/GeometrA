import base64
from flask import request, jsonify, render_template

from GeometrA import app
from GeometrA.src.Screen import *
from GeometrA.src.path import GEOMETRA_ROOT

@app.route('/GeometrA/Screen')
def getScreenshotPath():
    try:
        path = capture()
        return path
    except Exception as e:
        return str(e)

@app.route('/GeometrA/Screen/Crop', methods=['POST'])
def crop():
    return cropPhoto(request.form)

@app.route('/GeometrA/Screen/<image>')
def getImage(image):
    with open(GEOMETRA_ROOT + "/screenshot_pic/" + image, 'rb') as f:
        result = base64.b64encode(f.read())
    result = 'data:image/png;base64,' + str(result)[2:-1]
    return result

@app.route('/GeometrA/Screen/Size')
def getScreenSize():
    return Screen.getScreenSize()
