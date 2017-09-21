from tkinter import *
from Controller.Mouse import Mouse #getIMGfile

class ShowImageButton:
    def __init__(self, parent, n):
        self.showImage = Button(parent, command= self.ShowImageButtonClick, text="Show image", width=12)
        self.focus = n

    def ShowImageButtonClick(self):
        from TestCaseUI import TestCaseUI
        UI = TestCaseUI.getTestCaseUI()
        UI.focus = self.focus
        self.image = UI.ctrl.case.getSteps(UI.focus).getValue()
        print(self.image)
        self.image.show()
