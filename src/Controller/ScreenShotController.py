from PIL import Image, ImageTk
import threading
import sys
sys.path.append('../')
from adbRobot import ADBRobot
from DeviceCheck import Check

'''
Get Screenshot from device and return to UI
'''



class GetScreenShot:
    def __init__(self):
        self.screenShot = Image.open(ADBRobot().screenshot())

    def getScreenShot():
        _screenshot = GetScreenShot()
        # Set size  should be bootstrap
        _screenshot.setSize(450, 800)
        return ImageTk.PhotoImage(_screenshot.screenShot)

    def setSize(self, x, y):
        self.screenShot.thumbnail((x, y))

def screenShotTrigger():
    if not Check().checkDevices():
        return False
    return GetScreenShot.getScreenShot()