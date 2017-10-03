from tkinter import *
from PIL import ImageTk
from TestStepUI import TestStepUI
from LoadFile import LoadFile
from Action import *
import StepOperate
import Value

import sys

sys.path.append('../TestCase/')
from TestController import TestController

filePath = None


class TestCaseUI(Frame):
    __single = None

    def __init__(self, parent=None, *args, **kwargs):
        if TestCaseUI.__single:
            raise TestCaseUI.__single
        TestCaseUI.__single = self

        self.focus = 0

        self.ctrl = TestController()

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

    def valueModified(self, n):
        self.focus = n
        self.ctrl.setStep(n)

    def actionFocusIn(self, image=None):
        action = self.stepList[self.focus].action.get()

        if action == '':
            self.stepList[self.focus].value.grid_remove()
        elif action == 'TestCase':
            path = LoadFile().LoadTestCasePath()
            if (path is not None) and (path != ''):
                self.stepList[self.focus].value.delete(0, 'end')
                self.stepList[self.focus].value.insert('end', path)
        elif action == 'Click' or action == 'Assert Exist' or action == 'Assert Not Exist':
            Value.testCaseImage(self.stepList, self.focus, image)
        elif action == 'Loop End':
            self.stepList[self.focus].value.grid_remove()
            self.ctrl.setStep(self.focus)

    def executeButtonClick(self, n):
        self.ctrl.execute(n)

    def addStep(self, n):
        self.stepList.append(TestStepUI(self.listFrame, len(self.stepList)))
        self.ctrl.insertStep(n)
        StepOperate.insert(self.stepList, n)
        # self.reloadTestCaseUI()

    def removeStep(self, n):
        if len(self.stepList) > 1:
            StepOperate.remove(self.stepList, n)
            self.ctrl.removeStep(n)
            # self.reloadTestCaseUI()
        if n == len(self.stepList):
            self.stepList.append(TestStepUI(self.listFrame, n))

    def clearUI(self):
        while len(self.stepList) > 0:
            self.stepList[0].remove()
            self.stepList.pop(0)
        self.stepList.append(TestStepUI(self.listFrame, 0))

    def reloadTestCaseUI(self):
        _case = self.ctrl.case
        if _case is None: return
        self.clearUI()
        for i in range(_case.getSize()):
            self.stepList.append(TestStepUI(self.listFrame, i+1))
            act = _case.getSteps(i).getAction()
            val = _case.getSteps(i).getValue()
            self.stepList[i].action.set(act)
            self.actionSelect(i)
            if (str(val.__class__) == "<class 'PIL.PngImagePlugin.PngImageFile'>") | (str(val.__class__) == "<class 'PIL.Image.Image'>"):
                val.resize((100, 100))
                self._image = ImageTk.PhotoImage(val)
                self.stepList[i].value.create_image(0, 0, anchor=NW, image=self._image)
                self.stepList[i].value.image = self._image
                self.stepList[i].value.image = self._image
            elif val == '':
                pass
            else:
                self.stepList[i].value.insert(END, str(val))
