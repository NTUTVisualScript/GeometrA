from TestStep import Step
from Viewtest import TestAdepter
class TestCase:
    def __init__(self, n=0):
        self.stepList = []
        for i in range(0, n):
            self.stepList.append(Step())

    def getSize(self):
        return len(self.stepList)

    def getSteps(self, n=-1):
        if n == -1:
            return self.stepList
        return self.stepList[n]

    def setAction(self, n, action):
        self.stepList[n].setAction(action)

    def setValue(self, n, value):
        self.stepList[n].setValue(value)

    def insert(self, n):
        self.stepList.insert(n, Step())
