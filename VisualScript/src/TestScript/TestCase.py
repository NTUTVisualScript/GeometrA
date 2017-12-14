from TestScript.TestStep import Step
class TestCase:
    def __init__(self, n=0):
        self.stepDict = {}

    def getSize(self):
        return len(self.stepDict)

    def getSteps(self, n=-1):
        if n == -1:
            return list(self.stepDict.values())
        return self.stepDict[n]

    def setAction(self, n, action):
        self.stepDict[n].setAction(action)

    def getAction(self, n):
        self.stepDict[n].getAction()

    def setValue(self, n, value):
        self.stepDict[n].setValue(value)

    def getValue(self, n):
        self.stepDict[n].getValue()

    def setNode(self, n, node):
        self.stepDict[n].setNode(node)

    def getNode(self, n):
        self.stepDict[n].getNode()

    def setStep(self, n, act, val, node=None):
        self.stepDict[n].setStep(act, val, node)

    def insert(self, n=-1, step=None, act=None, val=None, node=None):
        if step == None:
            step = Step(act, val, node)
        if n == -1:
            n = self.getSize()
        for i in range(self.getSize(), n, -1):
            self.stepDict[i] = self.stepDict[i-1]
        self.stepDict[n] = step

    def append(self, n):
        try:
            for i in range(self.getSize(), n, -1):
                self.stepDict[i] = self.stepDict[i-1]
            del self.stepDict[n]
        except:
            pass

    # To let stepDict be continuous
    def refresh(self):
        removeList = []
        for i in self.stepDict:
            if self.stepDict[i].getAction() == '':
                removeList.append(i)
        for i in removeList:
            del self.stepDict[i]
        i = 0
        temp = {}
        for j in self.stepDict:
            temp[i] = self.stepDict[j]
            i = i+1
        self.stepDict = temp

    def delete(self, n):
        del self.stepDict[n]
        self.refresh()

    def setStatus(self, n, status):
        return self.stepDict[n].setStatus(status)

    def getStatus(self, n):
        return self.stepDict[n].getStatus()

    def clear(self):
        del self.stepDict
        self.stepDict = {}

    def copy(self):
        case = TestCase()
        for i in self.stepDict:
            case.insert(step=self.stepDict[i].copy())
        return case
