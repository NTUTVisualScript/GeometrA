from tkinter import *


class Mouse(Frame):
    def __init__(self, parent):
        self.mousePosition = StringVar()  #displays mouse position
        self.mousePosition.set( "Mouse outside the window")
        self.positionalLabel = Label(parent, textvariable = self.mousePosition)
        self.positionalLabel.pack( side = BOTTOM)

        parent.bind("<Button-1>", self.buttonPressed)
        parent.bind("<ButtonRelease-1>", self.buttonReleased)
        parent.bind("<B1-Motion>", self.mouseDragged)

    def buttonPressed(self, event):
        self.mousePosition.set("[ " + str(event.x) + " , " + str(event.y) + " ]")

    def buttonReleased(self, event):
        self.mousePosition.set("[ " + str(event.x) + " , " + str(event.y) + " ]")

    def mouseDragged(self, event):
        self.mousePosition.set("[ " + str(event.x) + " , " + str(event.y) + " ]")
