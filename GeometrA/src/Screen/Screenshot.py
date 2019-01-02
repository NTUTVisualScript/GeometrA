from PIL import Image, ImageFile
from GeometrA.src.ADB.adbRobot import ADBRobot

ImageFile.LOAD_TRUNCATED_IMAGES = True
class Screen:
    screenShot = None

    def __init__(self):
        self.path = ADBRobot().screenshot()
        size = Screen.getScreenSize()
        widthHeight = size.split('x')
        self.x = int(widthHeight[0])
        self.y = int(widthHeight[1])
        self.setSize(self.x, self.y)

    def setSize(self, x, y):
        Screen.screenShot = Image.open(self.path)
        Screen.screenShot.thumbnail((x, y))
        Screen.screenShot.save(self.path, "PNG")

    def getImagePath(self):
        return self.path

    @staticmethod
    def getScreenSize():
        return ADBRobot().get_device_size() #ex: 1920x1080
