from tkinter import *
from Controller.Mouse import Mouse #getIMGfile

class ShowImageButton:
    def __init__(self, parent):
        self.showImage = Button(parent, command= self.ShowImageButtonClick, text="Show image", width=12)

    def ShowImageButtonClick(self):
        self.image = Mouse.croppedPhoto
        self.image.show()
