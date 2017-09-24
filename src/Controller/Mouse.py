from tkinter import *
from PIL import Image, ImageTk
from Controller.ScreenShotController import GetScreenShot
from TestCaseUI import TestCaseUI
import math


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
        self.drawArrow(self.startX, self.startY, event.x, event.y)

    def mouseReleased(self, event):
        if GetScreenShot.screenShot == None: return
        self.cropPhoto(event)

    def cropPhoto(self, event):
        photo = Image.open('./screenshot_pic/tmp.png')
        width, height = photo.size

        self.startX = self.startX * width / 450
        self.startY = self.startY * height / 800
        self.endX = event.x * width / 450
        self.endY = event.y * height / 800

        UI = TestCaseUI.getTestCaseUI()
        if (self.startX < self.endX) and (self.startY < self.endY):
            Mouse.croppedPhoto = photo.crop((self.startX, self.startY, self.endX, self.endY))
            #left-top
        elif (self.startX < self.endX) and (self.startY > self.endY):
            Mouse.croppedPhoto = photo.crop((self.startX, self.endY, self.endX, self.startY))
            #left-bottom
        elif(self.startX > self.endX) and (self.startY < self.endY):
            Mouse.croppedPhoto = photo.crop((self.endX, self.startY, self.startX, self.endY))
            #right-top
        else:
            Mouse.croppedPhoto = photo.crop((self.endX, self.endY, self.startX, self.startY))
            #right-bottom
            
        UI.actionFocusIn(ImageTk.PhotoImage(Mouse.croppedPhoto.resize((100, 100))))
        UI.ctrl.setStep(UI.focus, Mouse.croppedPhoto)

    def drawArrow(self, startX, startY, endX, endY):
        angle = math.atan2(startY - endY, startX - endX) * 180 / math.pi
        angle1 = (angle + 30) * math.pi / 180
        angle2 = (angle - 30) * math.pi / 180
        topX = 30 * math.cos(angle1)
        topY = 30 * math.sin(angle1)
        botX = 30 * math.cos(angle2)
        botY = 30 * math.sin(angle2)

        self.block.create_line(startX, startY, endX, endY, fill="red", width=2)

        arrowX = endX + topX
        arrowY = endY + topY

        self.block.create_line(endX, endY, arrowX, arrowY, fill="red", width=2)

        arrowX = endX + botX
        arrowY = endY + botY

        self.block.create_line(endX, endY, arrowX, arrowY, fill="red", width=2)
