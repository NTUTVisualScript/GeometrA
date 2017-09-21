from TestCase import TestCase
from Executor import Executor
import threading

class TestController:
    def __init__(self):
        self.case = TestCase()
        self.exe = Executor(self.case)

    def execute(self, n):
        threading.Thread(target=self.exe.execute, args=(n,)).start()

    def runAll(self):
        threading.Thread(target=self.exe.runAll).start()

    def setStep(self, n, image = None):
        if n == None: return
        from TestCaseUI import TestCaseUI as UI
        stepList = UI.getTestCaseUI().stepList
        self.case.refresh()
        try:
            if image is None:
                self.case.getSteps(n).setValue(stepList[i].value.get())
            else:
                self.case.getSteps(n).setValue(image)
        except:
            try:
                if image is None:
                    self.case.insert(n=n, act=stepList[n].action.get(), val=stepList[n].value.get())
                else:
                    self.case.insert(n=n, act=stepList[n].action.get(), val=image)
            except Exception as e:
                print(str(e))
                return 'Invalid Value'

    def clearTestCase(self):
        from TestCaseUI import TestCaseUI as UI
        self.case.clear()
        UI.getTestCaseUI().reloadTestCaseUI()

    def ShowImageButtonClick(self):
        from TestCaseUI import TestCaseUI
        UI = TestCaseUI.getTestCaseUI()
        UI.focus = self.focus
        self.image = UI.ctrl.case.getSteps(UI.focus).getValue()
        print(self.image)
        self.image.show()
