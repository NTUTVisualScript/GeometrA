from TestStep import Step
class TestCase:
    def __init__(self, n=0):
        self.stepDict = {}
        for i in range(0, n):
            self.stepDict[i] = Step()

    def getSize(self):
        return len(self.stepDict)

    def getSteps(self, n=-1):
        if n == -1:
            return self.stepDict.values()
        return self.stepDict[n]

    def setAction(self, n, action):
        self.stepDict[n].setAction(action)

    def setValue(self, n, value):
        self.stepDict[n].setValue(value)

    def insert(self, n, step):
        self.stepDict[n] = step

    def delete(self, n):
        del self.stepDict[n]

    def setStatus(self, n, status):
        return self.stepDict[n].setStatus(status)

    def getStatus(self, n):
        return self.stepDict[n].getStatus()
