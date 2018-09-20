import base64
from flask import request, jsonify, render_template

from GeometrA import app
from GeometrA.src.Screen import *

@app.route('/GeometrA/Screen')
def getScreenshotPath():
    path = capture()
    return path

@app.route('/GeometrA/Screen/Crop', methods=['POST'])
def crop():
    return cropPhoto(request.form)

@app.route('/GeometrA/Screen/<image>')
def getImage(image):
    with open("./GeometrA/static/screenshot_pic/" + image, 'rb') as f:
        result = base64.b64encode(f.read())
    result = 'data:image/png;base64,' + str(result)[2:-1]
    return result

@app.route('/GeometrA/Screen/Size')
def getScreenSize():
    return Screen().getScreenSize()