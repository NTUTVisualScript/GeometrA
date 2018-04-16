from GeometrA import app
from GeometrA.src.Screen import capture

@app.route('/GeometrA/Screen')
def getScreenshotPath():
    return capture()

    
