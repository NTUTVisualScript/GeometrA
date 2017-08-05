from TestStep import Step
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
        try:
            self.stepList[n].setAction(action)
        except Exception:
            raise Exception('Not an action')

    def setValue(self, n, value):
        self.stepList[n].setValue(value)

    def insert(self, n):
        self.stepList.insert(n, Step())

    def delete(self, n):
        del self.stepList[n]

    def setStatus(self, n, status):
        return self.stepList[n].setStatus(status)

    def getStatus(self, n):
        return self.stepList[n].getStatus()
