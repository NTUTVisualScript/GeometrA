from tkinter import *
from adbRobot import ADBRobot
from PIL import Image, ImageTk

def Get_PhoneScreen():
    global filePath
    robot = ADBRobot()
    filePath = robot.screenshot()
    print(filePath)
    return filePath

class ScreenshotUI(Canvas):
    __single = None

    def __init__(self, parent=None, *args, **kwargs):
        Canvas.__init__(self, parent, *args, **kwargs,  height=800, width=450, borderwidth=-1, bg='white')
        self.before_image = None
        if ScreenshotUI.__single:
            raise ScreenshotUI.__single
            ScreenshotUI.__single = self

        self.place(x = 0, y = 30)

    def getScreenShotUI(parent):
        if not ScreenshotUI.__single:
            ScreenshotUI.__single = ScreenshotUI(parent)
        return ScreenshotUI.__single

    def set_ImageRank(self):
        print("rank")

    def getScreenShot(self):
        self.delete("all")
        self.LoadingFile()
        self.photo = Image.open(Get_PhoneScreen())
        self.photo_width, self.photo_height = self.photo.size
        self.photo.thumbnail((450, 800))
        self.width, self.height = self.photo.size
        self.multiple = self.photo_width / self.width
        self.screenshot_photo = ImageTk.PhotoImage(self.photo)
        self.message.InsertText("Loading finish\n")
        self.create_image(0, 0, anchor=NW, image = self.screenshot_photo)
        self.image = self.screenshot_photo

    def create_before_image(self):
        self.before_image = Canvas(self, height=800, width=450)
        self.before_image.configure(borderwidth=-3)
        self.before_image.place(x=0, y=0)

    def set_run_test_screenshot(self, photopath):
        print(photopath)
        before_action_image =Image.open(photopath)
        before_action_image.thumbnail((450, 800))
        beforeimage = ImageTk.PhotoImage(before_action_image)

        if self.before_image == None:
            self.create_before_image()

        self.before_image.create_image(0, 0, anchor=NW, image=beforeimage)
        self.before_image.image = beforeimage

    def remove_run_test_screenshot(self):
        if self.before_image is not None:
            self.before_image.delete("all")
            self.before_image.place_forget()
            self.before_image = None
