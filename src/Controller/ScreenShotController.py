from PIL import Image, ImageTk
import threading
import sys
sys.path.append('../')
from adbRobot import ADBRobot
from DeviceCheck import Check
from MessageUI import Message

'''
Get Screenshot from device and return to UI
'''



class GetScreenShot:
    screenShot = None
    def __init__(self):
        path = ADBRobot().screenshot()
        GetScreenShot.screenShot = Image.open(path)

    def capture():
        screenShot = GetScreenShot()
        # Set size  should be bootstrap
        screenShot.setSize(450, 800)
        return ImageTk.PhotoImage(GetScreenShot.screenShot)

    def setSize(self, x, y):
        GetScreenShot.screenShot.thumbnail((x, y))

def screenShotTrigger():
    if not Check().checkDevices():
        Message.getMessage().noDevice()
        return False
    Message.getMessage().capturing()
    capture = GetScreenShot.capture()
    Message.getMessage().getScreenShot()
    return capture
