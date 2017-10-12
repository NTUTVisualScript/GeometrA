from TestCase import TestCase
from Executor import Executor
import threading
from Record import *
import Value
from MessageUI import Message
from DeviceCheck import Check
from GUI.DialogueForm import  DialogueForm
from HTML.Report import Report

class TestController:
    def __init__(self):
        self.case = TestCase()
        self.exe = Executor(self.case)
        self.undo = Undo(self.case)
        self.redo = Redo()
        self.save = False

    def execute(self, n):
        threading.Thread(target=self.exe.execute, args=(n,)).start()

    def runButtonClick(self):
        if not self.save:
            error = 'Not Saved Error'
            notSavedMessage = 'Test case is not saved! '
            DialogueForm.Messagebox(error, notSavedMessage)
            return
        if not Check().checkDevices():
            Message.getMessage().noDevice()
            return
        from TestCaseUI import TestCaseUI as UI
        self.case.refresh()
        UI.getTestCaseUI().reloadTestCaseUI()
        threading.Thread(target=self.runCase).start()

    def runCase(self):
        self.report = Report()
        result = self.runAll()
        self.report.end(result, self.case.getSize())

    def runAll(self):
        i = 0
        ms = Message.getMessage()
        while i < self.case.getSize():
            step = self.case.getSteps(i)
            self.report.stepStart(step)
            status = self.exe.execute(i)
            self.report.stepEnd(step, i)
            loop = 'Loop Begin'
            if self.case.getSteps(i).getAction() == loop:
                i = self.exe.loopEnd(i)
            ms.stepState(i, status)
            f = 'Failed'
            e = 'Error'
            if (status == f) or status == e: return status
            i = i+1
        ms.caseSuccess()
        s = 'Success'
        return s

    def caseSaved(self, status):
        self.save = status

    def undoClick(self, event=None):
        from TestCaseUI import TestCaseUI as UI
        self.redo.push(self.case)
        self.case = self.undo.pop()
        UI.getTestCaseUI().reloadTestCaseUI()

    def redoClick(self, event=None):
        if self.redo.getSize() == 0: return

        from TestCaseUI import TestCaseUI as UI
        self.undo.push(self.case)
        self.case = self.redo.pop()
        UI.getTestCaseUI().reloadTestCaseUI()

    def insertStep(self, n):
        self.caseSaved(False)
        self.redo.reset()
        self.undo.push(self.case)
        empty = ''
        self.case.insert(n=n, act=empty, val=empty)

    def removeStep(self, n):
        self.caseSaved(False)
        self.redo.reset()
        self.undo.push(self.case)
        self.case.delete(n)

    def setStep(self, n, image = None):
        if n == None: return
        self.caseSaved(False)
        # Save current TestCase to undo model
        self.redo.reset()
        self.undo.push(self.case)

        stepExist = self.exist(n)
        self.putValue(n, stepExist, image)



        # Handle the exceptions for step n is not exist
    def exist(self, n):
        try:
            self.case.getSteps(n)
            return True
        except:
            return False


    # Set step information to model
    def putValue(self, n, stepExist, image):
        from TestCaseUI import TestCaseUI as UI
        stepList = UI.getTestCaseUI().stepList
        try:
            if stepExist:
                if image is None:
                    Value.testCaseEntryValid(stepList, n)
                    self.case.setAction(n, stepList[n].action.get())
                    self.case.setValue(n, stepList[n].value.get())
                else:
                    self.case.setAction(n, stepList[n].action.get())
                    self.case.setValue(n, image)
            else:
                if image is None:
                    Value.testCaseEntryValid(stepList, n)
                    self.case.insert(n=n, act=stepList[n].action.get(), val=stepList[n].value.get())
                else:
                    self.case.insert(n=n, act=stepList[n].action.get(), val=image)
        # Handle the exception for invalid value
        except Exception as e:
            print(e)
            Value.testCaseEntryError(stepList, n)


    def clearTestCase(self):
        from TestCaseUI import TestCaseUI as UI
        self.case.clear()
        UI.getTestCaseUI().clearUI()
        Message.getMessage().reset()

    def ShowImageButtonClick(self, n):
        image = self.case.getSteps(n).getValue()
        image.show()
