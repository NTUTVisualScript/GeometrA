from tkinter import *
from TestCaseUI import TestCaseUI
from TestController import TestController

class ClearButton:
    def __init__(self, parent = None):
        self._clearbutton = Button(parent, command=self.clearButtonClick, text="Clear Testcase", width=15)

    def showClearButton(self):
        self._clearbutton.place(x = 580, y = 270) #should use pack/grid instead of place

    def clearButtonClick(self):
        TestCaseUI.getTestCaseUI().ctrl.clearTestCase()

class RunButton:
    def __init__(self, parent=None):
        self._runButton = Button(parent, command=self.runButtonClick, text="Run", width=15)

    def showRunButton(self):
        self._runButton.place(x = 460, y=270)

    def runButtonClick(self):
        TestController().runAll()
