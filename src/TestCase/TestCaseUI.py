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
    def generateCaseBlock(self):
        n = self.case.getSize()

        # Generate one line at one time
        for i in range(0, n):
            num = Label(self.frame, text = str(i+1) + '. ', width = 3)
            self.addButtonList.append(Button(self.frame, command=lambda: self.addButtonClick(i), text='+', width=3))
            self.removeButtonList.append(Button(self.frame, command=lambda: self.removeButtonClick(i), text='-', width=3))
            self.executeButtonList.append(Button(self.frame, command=lambda: self.executeButtonClick(i, False), text='▶', width=3))

            self.actionMenuList.append(TestCaseAction(self.frame, textvariable=StringVar(), width=10, height=22, state='readonly'))

            self.actionMenuList[i].bind('<<ComboboxSelected>>', lambda event, j=i: self.actionSelect(i))
            self.actionMenuList[i].bind('<MouseWheel>', lambda event, j=i: self.actionSelect(i))

            self.valueBarList.append(TestCaseValue(self.frame, width=35))
            self.valueBarList[i].bind('<FocusIn>', lambda event, i=n: self.valueFocusIn(event, i))
            self.nodePathLIst.append(None)

            self.showImageList.append(Button(self.frame, command=lambda: self.showImageButtonClick(i), text="Show Image", width=12))

            num.grid(row = i+1, column = 1)
            self.addButtonList[i].grid(row = i+1, column = 2)
            self.removeButtonList[i].grid(row = i+1, column = 3)
            self.executeButtonList[i].grid(row = i+1, column = 4)
            self.actionMenuList[i].grid(row = i+1, column = 5, padx = (5, 0), pady = (5, 2.5))
            self.valueBarList[i].grid(row = i+1, column = 6, padx = (5, 0), pady = (5, 2.5))

    def addButtonClick(self, n):
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
            pass
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
