from tkinter import *
import threading
import Controller.ScreenShotController as SSCtrl
from Controller.Mouse import Mouse

class ScreenshotUI(Canvas):
    __single = None


    def __init__(self, parent=None, *args, **kwargs):
        Canvas.__init__(self, parent, *args, **kwargs,  height=800, width=450, borderwidth=-1, bg='white')

        self.mouse = Mouse(self, parent)

        if ScreenshotUI.__single:
            raise ScreenshotUI.__single
        ScreenshotUI.__single = self


        self.place(x = 0, y = 60)

    def getScreenshotUI(parent=None):
        if not ScreenshotUI.__single:
            ScreenshotUI.__single = ScreenshotUI(parent)
        return ScreenshotUI.__single

    def getScreenshot(self):
        self.delete("all")
        self.screenshot_photo = SSCtrl.screenShotTrigger()
        self.mouse.setOriginalFrame()
        self.create_image(0, 0, anchor=NW, image=self.screenshot_photo)
