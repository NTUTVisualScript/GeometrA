from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from TestCaseActionCombobox import TestCaseAction
from TestCaseEntry import TestCaseValue
from LoadFile import LoadFile

from TestCase import TestCase

class TestCaseUI():
    def __init__(self, frame):
        self.frame = frame
        self.case = TestCase()
        self.line = 50
        self.addButtonList = []
        self.removeButtonList = []
        self.executeButtonList = []
        self.actionMenuList = []
        self.valueBarList = []
        self.nodePathLIst = []
        self.showImageList = []

        self.generateCaseBlock()
        for i in range(50):
            generateStepBlock(i)

    # To generate the line of Test Step on the UI
    def generateStepBlock(self, n):
        num = Label(self.frame, text = str(n+1) + '. ', width = 3)
        self.addButtonList.append(Button(self.frame, command=lambda: self.addButtonClick(n), text='+', width=3))
        self.removeButtonList.append(Button(self.frame, command=lambda: self.removeButtonClick(n), text='-', width=3))
        self.executeButtonList.append(Button(self.frame, command=lambda: self.executeButtonClick(n, False), text='▶', width=3))

        # actions = ['', 'Click', 'Drag', 'Set Text', 'TestCase', 'Loop Begin', 'Loop End',
        #             'Sleep(s)', 'Android Keycode', 'Assert Exist', 'Assert Not Exist']
        self.actionMenuList.append(TestCaseAction(self.frame, 0, textvariable=StringVar(), width=10, height=22, state='readonly'))

        self.actionMenuList[n].bind('<<ComboboxSelected>>', lambda event, j=n: self.actionSelect(n))
        self.actionMenuList[n].bind('<MouseWheel>', lambda event, j=n: self.actionSelect(n))

        self.valueBarList.append(TestCaseValue(self.frame, width=35))
        self.valueBarList[n].bind('<FocusIn>', lambda event, i=n: self.valueFocusIn(event, i))
        self.nodePathLIst.append(None)

        self.showImageList.append(Button(self.frame, command=lambda: self.showImageButtonClick(n), text="Show Image", width=12))

        num.grid(row = n+1, column = 1)
        self.addButtonList[i].grid(row = n+1, column = 2)
        self.removeButtonList[i].grid(row = n+1, column = 3)
        self.executeButtonList[i].grid(row = n+1, column = 4)
        self.actionMenuList[i].grid(row = n+1, column = 5, padx = (5, 0), pady = (5, 2.5))
        self.valueBarList[i].grid(row = n+1, column = 6, padx = (5, 0), pady = (5, 2.5))

    def addButtonClick(self, n):
        self.line = self.line+1

        self.case.insert(n)
        self.generateCaseBlock()

    def removeButtonClick(self, n):
        self.case.delete(n)
        self.generateCaseBlock()

    def executeButtonClick(self, n):
        exe = Executor(self.case)
        exe.run(n)

    def actionSelect(self, n):
        self.focus = n
        self.case.setAction(n, self.actionMenuList[n].get())
        self.case.setValue(n, '')
        self.actionFocusIn(n)

    def valueFocusIn(self,event, n):
        self.focus = n
        if self.actionManuList[self.focus].get() != 'TestCase':
            self.Action_FocusIn()

    def actionFocusIn(self, n):
        action = self.actionMenuList[n].get()
        if action == 'Drag':

        elif action == 'TestCase':
            openfile = LoadFile()
            path = openfile.LoadTestCasePath()
            if (path is not None) & (path is not ''):
                self.valueBarList[n].delete(0, 'end')
                self.valueBarList[n].insert('end', path)
        elif (action == 'Click') | (action == 'Assert Exist') | (action == 'Assert Not Exist'):
            self.testStepImage()

    def testStepEntry(self, line):
        value = TestCaseValue(self.listFrame, width = 35)
        value.bind('<FocusIn>', lambda event, i=line: self.valueFocusIn(event, i))
        self.valueBarList[line].grid_remove()
        self.shoimageList[line].grid_remove()
        self.valueBarList[line] = value
        self.valueBarList[line].grid(row=ilne+1, column=6, padx=(5, 0), pady=(5, 2.5))

    def testStepImage(self, line, image = None):
        values_image = Canvas(self.frame, bg = '#FFFFFF', height=100, width=100)
        values_image.create_image(0, 0, anchor=NW, image=image)
        values_image.bind('<Button-1>', lambda event, i=line: self.valueFocusIn(event, i))
        values_image.image = image
        self.valueBarList[line].grid_remove()
        self.valueBarList[line] = values_image
        self.valueBarList[line].grid(row=line+1, column=6, padx=(5, 0), pady=(5, 2.5))
        self.showImageList[line].grid(row=line + 1, column=7, padx=(5, 0), pady=(5, 2.5))
