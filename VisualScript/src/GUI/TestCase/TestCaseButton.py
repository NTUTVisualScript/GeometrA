from tkinter import *
from VisualScript.src.GUI.TestCase.TestCaseUI import TestCaseUI

class ClearButton:
    def __init__(self, parent = None):
        self._clearbutton = Button(parent, command=self.clearButtonClick, text="Clear Testcase", width=15)
        self.showClearButton()

    def showClearButton(self):
        self._clearbutton.place(x = 580, y = 270) #should use pack/grid instead of place

    def clearButtonClick(self):
        TestCaseUI.getTestCaseUI().ctrl.clearTestCase()

class RunButton(ClearButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._runButton = Button(parent, command=self.runButtonClick, text="Run", width=15)
        self.showRunButton()

    def showRunButton(self):
        self._runButton.place(x = 460, y=270)

    def runButtonClick(self):
        TestCaseUI.getTestCaseUI().ctrl.runButtonClick()

class TestCaseButton(RunButton):
    __single = None
    def __init__(self, parent=None):
        if TestCaseButton.__single:
            raise TestCaseButton.__single
        TestCaseButton.__single = self
        super().__init__(parent)

    def getTestCaseButton(parent=None):
        if not TestCaseButton.__single:
            TestCaseButton.__single = TestCaseButton(parent)
        return TestCaseButton.__single
