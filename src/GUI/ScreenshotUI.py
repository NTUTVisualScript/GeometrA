from tkinter import *
import threading
from adbRobot import ADBRobot
from PIL import Image, ImageTk
import Controller.ScreenShotController as SSCtrlr
from Controller.ScreenShotController import GetScreenShot

class ScreenshotUI(Canvas):
    __single = None

    def __init__(self, parent=None, *args, **kwargs):
        Canvas.__init__(self, parent, *args, **kwargs,  height=800, width=450, borderwidth=-1, bg='white')
        self.ButtonGetScreenshot()
        self.before_image = None
        if ScreenshotUI.__single:
            raise ScreenshotUI.__single
        ScreenshotUI.__single = self


        self.place(x = 0, y = 30)

    def getScreenshotUI(parent=None):
        if not ScreenshotUI.__single:
            ScreenshotUI.__single = ScreenshotUI(parent)
        return ScreenshotUI.__single

    def getScreenshot(self):
        self.delete("all")
        self.screenshot_photo = GetScreenShot.getScreenShot()
        self.create_image(0, 0, anchor=NW, image=self.screenshot_photo)

    def ButtonGetScreenshot(self):
        self.dumpUI = Button(self.master, command=lambda :threading.Thread(target=self.getScreenshot).start(), text="Get Screenshot", width=15)
        self.dumpUI.place(x=0, y=3)