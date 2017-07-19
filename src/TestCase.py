from TestCaseStep import Step
from Viewtest import TestAdepter
class TestCase:
    def __init__(self, n=0):
        self.stepList = []
        self.stepSize = n
        for i in range(0, n):
            stepList.append(Step())

    def insert(self, n):
        self.stepList.insert(n, Step())
