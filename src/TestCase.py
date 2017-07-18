from TestCaseStep import Step
from Viewtest import TestAdepter
class TestCase:
    def __init__(self):
        self.steplist = []

    def insert(self, n , action, value, image, path):
        self.steplist.insert(n, Step(action, value, image, path))

    def run(self):
        # TestAdepter.set_data()
        #TestAdepter.run_all()
