import base64

from GeometrA import app
from GeometrA.src.Screen import capture

@app.route('/GeometrA/Screen')
def getScreenshotPath():
    return capture()

@app.route('/GeometrA/Screen/Crop', methods=['POST'])
def crop():
    return "./GeometrA/static/screenshot_pic/tmp.png"

@app.route('/GeometrA/Screen/<image>')
def getImage(image):
    with open("./GeometrA/static/screenshot_pic/" + image, 'rb') as f:
        result = base64.b64encode(f.read())
    result = 'data:image/png;base64,' + str(result)[2:-1]
    return result
