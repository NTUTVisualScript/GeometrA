from GUI.ScreenShotUI import ScreenshotUI

class ScreenShot(ScreenshotUI):
    __single = None
    def __init__(self):
        if ScreenShot.__single:
            raise ScreenShot.__single
            ScreenShot.__single = self


    def getScreenShot(parent):
        if not ScreenShot.__single:
            ScreenShot.__single = ScreenShot(parent)
        return ScreenShot.__single



