from PIL import Image
import threading
import sys
sys.path.append('../')
from adbRobot import ADBRobot

'''
Get Screenshot from device and return to UI
'''



class GetScreenShot:
    def __init__(self):
        self.screenShot = Image.open(ADBRobot().screenshot())

    def getScreenShot():
        screenShot = GetScreenShot()
        # Set size  should be bootstrap
        screenShot.setSize(450, 800)
        return screenShot.screenShot

    def setSize(self, x, y):
        self.screenShot.thumbnail(x, y)

def screenShotTrigger():
    threading.Thread(target=GetScreenShot().getScreenShot)
