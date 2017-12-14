from tkinter import *
from TestCaseActionCombobox import TestCaseAction
from TestCaseEntry import TestCaseValue

import sys
sys.path.append('../../TestCase/')

class TestStepUI():
    def __init__(self, parent, n):
        from TestCaseUI import TestCaseUI
        from Controller.TestController import TestController
        self.parent = parent
        self.num = n
        self.lineNum = Label(self.parent, text=str(self.num + 1) + ". ", width=3)

        self.addButton = Button(self.parent, text="+", width=3, \
                                command=lambda: TestCaseUI.getTestCaseUI().addStep(self.num))

        self.removeButton = Button(self.parent, text="-", width=3, \
                                   command=lambda: TestCaseUI.getTestCaseUI().removeStep(self.num))

        self.executeButton = Button(self.parent, text="▶", width=3,
                command=lambda:TestCaseUI.getTestCaseUI().executeButtonClick(self.num))

        self.action = TestCaseAction(self.parent, textvariable=StringVar(), width=10, height=22,
                                     state='readonly')
        self.action.bind("<<ComboboxSelected>>", lambda event: TestCaseUI.getTestCaseUI().actionSelect(self.num))
        self.action.bind("<MouseWheel>", lambda event: TestCaseUI.getTestCaseUI().actionSelect(self.num))

        self.value = TestCaseValue(self.parent, width=35)

        self.showImage = Button(self.parent, command=lambda: TestCaseUI.getTestCaseUI().ctrl.ShowImageButtonClick(self.num), text="Show image", width=12)

        self.lineNum.grid(row=self.num + 1, column=1)
        self.addButton.grid(row=self.num + 1, column=2)
        self.removeButton.grid(row=self.num + 1, column=3)
        self.executeButton.grid(row=self.num + 1, column=4)
        self.action.grid(row=self.num + 1, column=5, padx=(5, 0), pady=(5, 2.5))

    def remove(self):
        self.lineNum.grid_remove()
        self.action.grid_remove()
        self.value.grid_remove()
        self.addButton.grid_remove()
        self.removeButton.grid_remove()
        self.executeButton.grid_remove()
        self.showImage.grid_remove()
