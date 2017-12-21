'''
Get Screenshot from device and return to UI
'''

from PIL import Image, ImageTk
import threading
from VisualScript.src.ADB.adbRobot import ADBRobot
from VisualScript.src.Controller.DeviceCheck import Check
from VisualScript.src.GUI.MessageUI import Message

class GetScreenShot:
    x = 450
    y = 800
    multiple = 1080/x

    screenShot = None
    def __init__(self):
        path = ADBRobot().screenshot()
        GetScreenShot.screenShot = Image.open(path)

    def capture():
        screenShot = GetScreenShot()
        # Set size  should be bootstrap
        screenShot.setSize(GetScreenShot.x, GetScreenShot.y)
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
