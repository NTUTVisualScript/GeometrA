from tkinter import *
from TestCaseActionCombobox import TestCaseAction
from TestCaseEntry import TestCaseValue

import sys
sys.path.append('../../TestCase/')

class TestStepUI():
    def __init__(self, parent, n):
        from TestCaseUI import TestCaseUI
        from ShowImageButton import ShowImageButton
        self.parent = parent

        self.lineNum = Label(self.parent, text=str(n + 1) + ". ", width=3)

        self.addButton = Button(self.parent, text="+", width=3, \
                                command=lambda :TestCaseUI.getTestCaseUI().addStep(n))

        self.removeButton = Button(self.parent, text="-", width=3, \
                                   command=lambda :TestCaseUI.getTestCaseUI().removeStep(n))

        self.executeButton = Button(self.parent, text="▶", width=3, \
                command=lambda :TestCaseUI.getTestCaseUI().executeButtonClick(n))

        self.action = TestCaseAction(self.parent, textvariable= StringVar(), width=10, height=22,
                                     state='readonly')
        self.action.bind("<<ComboboxSelected>>", lambda event:TestCaseUI.getTestCaseUI().actionSelect(n))
        self.action.bind("<MouseWheel>", lambda event:TestCaseUI.getTestCaseUI().actionSelect(n))

        self.value = TestCaseValue(self.parent, width=35)
        self.value.bind("<FocusIn>", lambda event: TestCaseUI.getTestCaseUI().valueFocusIn(n))

        self.showImage = ShowImageButton(self.parent).showImage #Button(parent, command=lambda: self.ShowimageButtonClick(n), text="show image", width=12)

        self.lineNum.grid(row=n + 1, column=1)
        self.addButton.grid(row=n + 1, column=2)
        self.removeButton.grid(row=n + 1, column=3)
        self.executeButton.grid(row=n + 1, column=4)
        self.action.grid(row=n + 1, column=5, padx=(5, 0), pady=(5, 2.5))

    def remove(self):
        self.lineNum.grid_remove()
        self.action.grid_remove()
        self.value.grid_remove()
        self.addButton.grid_remove()
        self.removeButton.grid_remove()
        self.executeButton.grid_remove()
        self.showImage.grid_remove()
