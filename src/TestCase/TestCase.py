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

    # def insert(self, n = -1):
    #     if(n == -1):
    #         step = Step()
    #         step.setSequence(self.getSize())
    #         self.stepList.append(step)
    #     elif n < self.getSize():
    #         for i in range(n+1, self.getSize()):
    #             self.stepList[i].setSequence(self.stepList[i].getSequence() + 1)
    #         self.stepList.insert(n+1, Step())
    #     else:
    #         raise Exception('Input Out Of Range')

    def insert(self, step):
        if self.getSize() == 0:
            self.stepList.append(step)
        else:
            for i in range(self.getSize()):
                if self.stepList[i].getSequence() > step.getSequence():
                    self.stepList.insert(i, step)
                    break

    def delete(self, n):
        del self.stepList[n]

    def setStatus(self, n, status):
        return self.stepList[n].setStatus(status)

    def getStatus(self, n):
        return self.stepList[n].getStatus()
