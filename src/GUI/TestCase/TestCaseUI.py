from tkinter import *
from TestStepUI import TestStepUI
from TestCaseActionCombobox import TestCaseAction
from TestCaseEntry import TestCaseValue
from LoadFile import LoadFile
from Action import *
import Click
import Value

import sys
sys.path.append('../TestCase/')
from TestCase import TestCase
from TestStep import Step
from Executor import Executor

filePath = None

class TestCaseUI(Frame):
    __single = None

    def __init__(self, parent = None, *args, **kwargs):
        if TestCaseUI.__single:
            raise TestCaseUI.__single
            TestCaseUI.__single = self
        self.case = TestCase()
        self.exe = Executor(self.case)

        Frame.__init__(self, parent, *args, **kwargs, borderwidth =2 ,relief = 'sunken')

        self.canvas = Canvas(self)
        self.listFrame = Frame(self.canvas)

        self.scrollb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollb.pack(side='right', fill='y')
        self.canvas['yscrollcommand'] = self.scrollb.set

        self.canvas.create_window((0, 0), window=self.listFrame, anchor='nw')
        self.listFrame.bind("<Configure>", self.AuxscrollFunction)
        self.scrollb.grid_forget()

        self.canvas.pack(side="left")
        self.place(x=460, y=300)

        self.swipeImage = None
        self.stepList = []
        self.stepList.append(TestStepUI(self.listFrame, 0))

    def getTestCaseUI(parent=None):
        if not TestCaseUI.__single:
            TestCaseUI.__single = TestCaseUI(parent)
        return TestCaseUI.__single

    def AuxscrollFunction(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=650, height=525)

    def actionSelect(self, n):
        self.focus = n
        if n == (len(self.stepList)-1):
            self.stepList.append(TestStepUI(self.listFrame, len(self.stepList)))
        Value.testCaseEntry(self.stepList, n)
        self.actionFocusIn()

    def valueFocusIn(self, n):
        self.focus = n
        if self.stepList[n].action.get() != 'TestCase':
            self.actionFocusIn()

    def actionFocusIn(self):
        action = self.stepList[self.focus].action.get()

        if (action != 'Swipe') & (self.swipeImage != None):
            self.swipeImage.place_forget()
            self.swipeImage = None

        if action == 'Swipe':
            if filePath is None: return
            '''
                Swipe could be acceptance after dumpUI and Screenshot are done.
                And here should be modified after they are done.
            '''
            self.swipeImage = Swipe()
        elif action == 'TestCase':
            path = LoadFile().LoadTestCasePath()
            if (path is not None) and (path != ''):
                self.stepList[self.focus].value.delete(0, 'end')
                self.stepList[self.focus].value.insert('end', path)
                self.case.setValue(self.focus, path)
        elif action == 'Click' or action == 'Assert Exist' or action == 'Assert Not Exist':
            Value.testCaseImage(self.stepList, self.focus)
        else:
            self.case.setValue(self.focus, self.stepList[self.focus].value.get())

    def executeButtonClick(self, n):
        self.exe.run(n)

    def addButtonClick(self, n):
        self.stepList.append(TestStepUI(self.listFrame, len(self.stepList)))
        Click.insert(self.stepList, n)

    def removeButtonClick(self, n):
        if len(self.stepList) > 1:
            Click.remove(self.stepList, n)
        if n == len(self.stepList):
            self.stepList.append(TestStepUI(self.listFrame, n))
