from TestCase import TestCase
from Executor import Executor
import threading

class TestController:
    def __init__(self):
        self.case = TestCase()
        self.exe = Executor(self.case)

    def execute(self, n):
        # self.loadCase()
        threading.Thread(target=self.exe.execute, args=(n,)).start()

    def runAll(self):
        # self.loadCase()
        threading.Thread(target=self.exe.runAll).start()

    def loadCase(self):
        from TestCaseUI import TestCaseUI as UI
        self.case.refresh()
        try:
            stepList = UI.getTestCaseUI().stepList
            for i in range(len(stepList)):
                self.case.insert(n=i, act=stepList[i].action.get(), val=stepList[i].value.get())
        except Exception as e:
            print(str(e))
            return 'Invalid Value'

    def setStep(self, n):
        from TestCaseUI import TestCaseUI as UI
        stepList = UI.getTestCaseUI().stepList
        self.case.refresh()
        try:
            self.case.getSteps(n).setValue(stepList[i].value.get())
        except:
            try:
                self.case.insert(n=n, act=stepList[n].action.get(), val=stepList[n].value.get())
            except Exception as e:
                print(str(e))
                return 'Invalid Value'

