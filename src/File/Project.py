from File.TestSuite import TestSuite

class Project:
    def __init__(self, suites):
        self.suites = {}
        self.getSuites(suites)

    def getSuites(self, suites):
        for suite in suites:
            self.suites[suite] = TestSuite(suites[suite])
            
