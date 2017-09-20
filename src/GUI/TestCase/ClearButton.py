from tkinter import *
from TestCaseUI import TestCaseUI

class ClearButton:
    def __init__(self, parent = None):
        self._clearbutton = Button(parent, command=self.clearButtonClick, text="Clear Testcase", width=15)

    def showClearButton(self):
        self._clearbutton.place(x = 580, y = 270) #should use pack/grid instead of place

    def clearButtonClick(self):
        TestCaseUI.getTestCaseUI().clearTestCaseUI()