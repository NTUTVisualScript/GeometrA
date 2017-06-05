from tkinter import *


class TestCaseImage(Canvas):
    def __init__(self, parent, *args, **kwargs):
        Canvas.__init__(self, parent, *args, **kwargs)
        self.create_image(0, 0, anchor=NW)

    def setImage(self, image):
        self.image = image
