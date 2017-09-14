import sys
sys.path.append('../')
from adbRobot import ADBRobot
from PIL import Image, ImageTk

'''
Get Screenshot from device and return to UI
'''

class GetScreenShot:
    def __init__(self):
        self.screenShot = Image.open(ADBRobot().screenshot())

    def screenShotTrigger():
        screenShot = GetScreenShot()
        # Set size  should be bootstrap
        screenShot.setSize(450, 800)
        return screenShot.screenShot

    def setSize(self, x, y):
        self.screenShot.thumbnail(x, y)
