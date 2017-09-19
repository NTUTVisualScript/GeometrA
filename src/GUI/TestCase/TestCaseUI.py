from tkinter import *
from PIL import Image, ImageTk
from TestStepUI import TestStepUI
from TestCaseActionCombobox import TestCaseAction
from TestCaseEntry import TestCaseValue
from LoadFile import LoadFile
from Action import *
import StepOperate
import Value
import threading

import sys

sys.path.append('../TestCase/')
from TestCase import TestCase
from TestStep import Step
from Executor import Executor

filePath = None


class TestCaseUI(Frame):
    __single = None

    def __init__(self, parent=None, *args, **kwargs):
        if TestCaseUI.__single:
            raise TestCaseUI.__single
        TestCaseUI.__single = self
        self.case = TestCase()
        self.exe = Executor(self.case)

        Frame.__init__(self, parent, *args, **kwargs, borderwidth=2, relief='sunken')

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
        if TestCaseUI.__single == None:
            TestCaseUI.__single = TestCaseUI(parent)
        return TestCaseUI.__single

    def AuxscrollFunction(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=650, height=525)

    def actionSelect(self, n):
        self.focus = n
        if n == (len(self.stepList) - 1):
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
            '''
            self.swipeImage = Swipe()
        elif action == '':
            self.stepList[self.focus].value.grid_remove()
        elif action == 'TestCase':
            path = LoadFile().LoadTestCasePath()
            if (path is not None) and (path != ''):
                self.stepList[self.focus].value.delete(0, 'end')
                self.stepList[self.focus].value.insert('end', path)
        elif action == 'Click' or action == 'Assert Exist' or action == 'Assert Not Exist':
            '''
                Here could be acceptance after dumpUI and ScreenShot or Tree_info are done.
            '''
            Value.testCaseImage(self.stepList, self.focus)
        elif action == 'Loop End':
            self.stepList[self.focus].value.grid_remove()
            # elif action == 'Loop Begin':
            #     Loop(self.stepList, self.focus)

    def executeButtonClick(self, n):
        try:
            self.case.insert(n=n, act=self.stepList[n].action.get(), val=self.stepList[n].value.get())
            if self.case.getSteps(n).getAction() == 'Loop Begin':
                i = 1
                j = n + 1
                while i != 0:
                    act = self.stepList[j].action.get()
                    if act == 'Loop End':
                        i = i - 1
                    elif act == 'Loop Begin':
                        i = i + 1
                    self.case.insert(n=j, act=act, val=self.stepList[j].value.get())
                    j = j + 1
            threading.Thread(target=self.exe.run, args=(n,)).start()
        except Exception as e:
            print(str(e))
            return 'Invalid Value!'

    def addStep(self, n):
        self.stepList.append(TestStepUI(self.listFrame, len(self.stepList)))
        StepOperate.insert(self.stepList, n)

    def removeStep(self, n):
        if len(self.stepList) > 1:
            StepOperate.remove(self.stepList, n)
        if n == len(self.stepList):
            self.stepList.append(TestStepUI(self.listFrame, n))

    def clearTestCaseUI(self):
        i = len(self.stepList)
        while i >= 0:
            self.removeStep(i)
            i = i - 1
        self.case.refresh()

    def reloadTestCaseUI(self, case=None):
        if not case is None:
            self.case = case
        self.clearTestCaseUI()
        for i in range(self.case.getSize()):
            action = self.case.getSteps(i).getAction()
            value = self.case.getSteps(i).getValue()
            self.stepList[i].action.set(action)
            self.actionSelect(i)
            if (action == 'Click' or action == 'Assert Exist' or action == 'Assert Not Exist'):

                self.stepList[i].value.insert(END, str(value))
            else:
                self.stepList[i].value.insert(END, str(value))
