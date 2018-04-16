from PIL import Image
from GeometrA.src.ADB.adbRobot import ADBRobot

class Screen:
    x = 1080
    y = 1920
    screenShot = None

    def __init__(self):
        self.path = ADBRobot().screenshot()
        self.setSize(Screen.x, Screen.y)

    def setSize(self, x, y):
        Screen.screenShot = Image.open(self.path)
        Screen.screenShot.thumbnail((x, y))
        Screen.screenShot.save(self.path, "PNG")

    def getImagePath(self):
        return self.path
