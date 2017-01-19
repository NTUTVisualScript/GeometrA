from tkinter import *
from adb_roboot import ADBRobot
from PIL import Image, ImageTk
from NotificationSenter import Singleton
import os

ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(ROOT_DIR, "screenshot_pic")

filePath = None

def IMG_PATH(name):
    return os.path.join(RESOURCES_DIR, name)

def Get_PhoneScreen():
    global filePath
    robot = ADBRobot()
    filePath = IMG_PATH(robot.screenshot())
    print(filePath)
    return filePath

class dumpScreenShot(Frame):

    def ScreenShotUI(self):
        self.screenshot = Canvas(self.master, bg='white', height=800, width=450)
        self.screenshot.grid(row=3, column=0, rowspan=50, columnspan = 25)
        self.multiple = 1

    def getScreenShot(self):
        self.photo = Image.open(Get_PhoneScreen())
        self.photo_width, self.photo_height = self.photo.size
        print(str(self.photo_width) + " , " + str(self.photo_height))
        self.photo.thumbnail((450, 800))
        self.width, self.height = self.photo.size
        self.multiple = self.photo_width / self.width
        print(str(self.multiple))
        self.screenshot_photo = ImageTk.PhotoImage(self.photo)
        self.screenshot.create_image(0, 0, anchor=NW, image=self.screenshot_photo)

    def getImgPath(self):
        return filePath

    def getCropRange(self):
        return self.left, self.top, self.right, self.bottom, self.multiple

    def resetScreenShot(self):
        self.screenshot.delete("all")
        self.screenshot.create_image(0, 0, anchor=NW, image=self.screenshot_photo)

    def cropImage(self, left, top, right, bottom):
        self.cropped = self.photo.crop((left, top, right, bottom))
        self.cropped.thumbnail((200, 200))
        self.tk_im = ImageTk.PhotoImage(self.cropped)
        #self.crop.create_image(0, 0, anchor=NW, image=self.tk_im)

    def drawRectangle(self, left, top, right, bottom):
        self.screenshot.create_rectangle(left +3 , top + 3 , right -3 , bottom -3 , outline='red', width=2)

    def getmouseEvent(self):
        self.mousePosition = StringVar()  # displays mouse position
        self.mousePosition.set("Mouse outside window")
        self.positionLabel = Label(self.master, textvariable=self.mousePosition)
        self.positionLabel.grid(column=25 + 1, row=20, columnspan=20)
        self.screenshot.bind("<Button-1>", self.clickdown)  # clickdown
        self.screenshot.bind("<ButtonRelease-1>", self.clickup)  # clickup
        self.screenshot.bind("<Motion>", self.motion)  #get mouse coordination
        # self.screenshot.bind("<Enter>", self.enteredWindow)
        # self.screenshot.bind("<Leave>", self.exitedWindow)
        self.screenshot.bind("<B1-Motion>", self.mouseDragged)  #滑鼠拖拉動作

    def clickdown(self, event):
        if filePath is None: return
        self.resetScreenShot()
        self.clickstartX = event.x
        self.clickstartY = event.y

    def clickup(self, event):
        if filePath is None: return
        self.clickendX = event.x
        self.clickendY = event.y
        self.left, self.right = sorted([self.clickendX, self.clickstartX])
        self.top, self.bottom = sorted([self.clickstartY, self.clickendY])

        self.cropImage(self.left, self.top, self.right, self.bottom)

    def motion(self,event):
        self.mousePosition.set("Mouse in window [ " + str(event.x * self.multiple) + ", " + str(event.y * self.multiple) + " ]")
        singleton = Singleton.getSingleton()
        singleton.doSomething()

    def mouseDragged(self, event):
        if filePath is None: return
        self.screenshot.create_image(0, 0, anchor=NW, image=self.screenshot_photo)
        if event.x < 0 :
            event.x = 0
        if event.y < 0 :
            event.y = 0
        if event.x > self.screenshot_photo.width():
            event.x = self.screenshot_photo.width()
        if event.y > self.screenshot_photo.height():
            event.y = self.screenshot_photo.height()

        self.drawRectangle(self.clickstartX, self.clickstartY, event.x, event.y )
        self.mousePosition.set("Rectangle at [ " + str(self.clickstartX * self.multiple ) + ", " + str(self.clickstartY * self.multiple) + " To " + str(event.x * self.multiple) + ", " + str(event.y * self.multiple) + " ]")
