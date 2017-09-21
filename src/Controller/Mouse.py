from tkinter import *
from PIL import Image, ImageTk
from Controller.ScreenShotController import GetScreenShot
from TestCaseUI import TestCaseUI


class Mouse():
    croppedPhoto = None
    def __init__(self, block, parent):
        self.mousePosition = StringVar()  #displays mouse position
        self.mousePosition.set( "Mouse outside the window")
        self.positionalLabel = Label(parent, textvariable = self.mousePosition)
        self.positionalLabel.place(x=150, y=30)

        self.block = block

        self.originalFrame = None

        self.block.bind("<Motion>", self.motion)
        self.block.bind("<Button-1>", self.clickDown)
        self.block.bind("<ButtonRelease-1>", self.mouseReleased)
        self.block.bind("<B1-Motion>", self.mouseDragged)
        self.block.bind("<Leave>", self.mouseLeave)

    def mouseLeave(self, event):
        if GetScreenShot.screenShot == None: return

        self.block.delete("all")
        self.block.create_image(0, 0, anchor=NW, image=self.originalFrame)
        self.block.screenshot_photo = self.originalFrame

    def motion(self, event):
        self.mousePosition.set("[ " + str(event.x) + " , " + str(event.y) + " ]")

    def clickDown(self, event):
        self.startX = event.x
        self.startY = event.y

    def setOriginalFrame(self):
        self.originalFrame = self.block.screenshot_photo

    def mouseDragged(self, event):
        if GetScreenShot.screenShot == None: return

        self.mouseLeave(event)

        if event.x < 0:
            event.x = 0
        if event.y < 0:
            event.y = 0
        if event.x > 450:
            event.x = 450
        if event.y > 800:
            event.y = 800

        self.motion(event)

        self.block.create_rectangle(self.startX, self.startY, event.x, event.y, outline ="red", width = 2)

    def mouseReleased(self, event):
        if GetScreenShot.screenShot == None: return
        photo = GetScreenShot.screenShot


        UI = TestCaseUI.getTestCaseUI()
        if (self.startX < event.x) and (self.startY < event.y):
            Mouse.croppedPhoto = photo.crop((self.startX, self.startY, event.x, event.y))
            #left-top
        elif (self.startX < event.x) and (self.startY > event.y):
            Mouse.croppedPhoto = photo.crop((self.startX, event.y, event.x, self.startY))
            #left-bottom
        elif(self.startX > event.x) and (self.startY < event.y):
            Mouse.croppedPhoto = photo.crop((event.x, self.startY, self.startX, event.y))
            #right-top
        else:
            Mouse.croppedPhoto = photo.crop((event.x, event.y, self.startX, self.startY))
            #right-bottom



        UI.actionFocusIn( ImageTk.PhotoImage(Mouse.croppedPhoto.resize((100, 100))))
        UI.ctrl.setStep(UI.focus, Mouse.croppedPhoto)
