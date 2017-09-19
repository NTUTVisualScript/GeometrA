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
        GetScreenShot.path = ADBRobot().screenshot()
        self.screenShot = Image.open(GetScreenShot.path)

    def capture():
        screenShot = GetScreenShot()
        # Set size  should be bootstrap
        screenShot.setSize(450, 800)
        return ImageTk.PhotoImage(screenShot.screenShot)

    def setSize(self, x, y):
        self.screenShot.thumbnail((x, y))

def screenShotTrigger():
    if not Check().checkDevices():
        return False
    return GetScreenShot.capture()