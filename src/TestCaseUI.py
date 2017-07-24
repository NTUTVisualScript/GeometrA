from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from TestStepUI import TestStepUI
from TestCaseActionCombobox import TestCaseAction
from TestCaseEntry import TestCaseValue

class TestCaseUI():
    def __init__(self, frame):
        self.frame = frame
        self.case = TestCase(50)
        self.addButtonList = []
        self.removeButtonList = []
        self.executeButtonList = []
        self.actionMenuList = []
        self.valueBarList = []
        self.nodePathLIst = []
        self.showImageList = []

        self.generateCaseBlock()

    # To generate the block on the UI for Test Case
    def generateCaseBlock():
        n = self.case.stepSize

        # Generate one line at one time
        for i in range(0, n):
            num = Label(self.listFrame, text = str(i+1) + '. ', width = 3)
            self.addButtonList.append(Button(self.frame, command=lambda: self.addButtonClick(i), text='+', width=3))
            self.removeButtonList.append(Button(self.frame, command=lambda: self.removeButtonClick(i, False), text='-', width=3))
            self.executeButtonList.append(Button(self.frame, command=lambda: self.executeButtonClick(i, False), text='▶', width=3))

            self.actionMenuList.append(TestCaseAction(self.frame, textvariable=StringVar(), width=10, height=22, state='readonly'))
            self.actionMenuList[i].bind('<<ComboboxSelected>>', lambda event, j=i: self.actionSelect(event, i))
            self.actionMenuList[i].bind('<MouseWheel>', lambda event, j=i: self.actionSelect(event, i))

            self.valueBarList.append(TestCaseValue(self.listFrame, width=35))
            self.valueBarList[i].bind('<FocusIn>', lambda event, i=n: self.valueFocusIn(event, i))
            self.nodePathLIst.append(None)

            self.showImageList.append(Button(self.frame, command=lambda: self.showImageButtonClick(i), text="Show Image", width=12))

            num.grid(row = i+1, column = 1)
            self.addButtonList[i].grid(row = i+1, column = 2)
            self.removeButtonList[i].grid(row = i+1, column = 3)
            self.executeButtonList[i].grid(row = i+1, column = 4)
            self.actionMenuList[i].grid(row = i+1, column = 5, padx = (5, 0), pady = (5, 2.5))
            self.valueBarList[i].grid(row = i+1, column = 6, padx = (5, 0), pady = (5, 2.5))

    def addButtonClick():



    def actionSelect(self, event, n):
        self.focus = n
