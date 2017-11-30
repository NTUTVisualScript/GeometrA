from File.TestSuite import TestSuite
import os, shutil

class Project:
    def __init__(self, path, suites):
        self.path = path
        self.check(suites)
        self.suites = {}
        self.getSuites(suites)

    def getSuites(self, suites):
        for suite in suites:
            self.suites[suite] = TestSuite(suites[suite], self.path + '/' + suite)

    def check(self, suites):
        notExist= []
        for suite in suites:
            path = self.path + '/' + suite
            if not os.path.isdir(path):
                notExist.append(suite)
        for suite in notExist:
            suites.pop(suite)

    def rename(self, origin, new):
        if new in self.suites:
            raise Exception('Suite already exists')
        self.suites[new] = self.suites.pop(origin)
        os.rename(self.path + '/' + origin, self.path + '/' + new)

    def delete(self, suite):
        self.suites.pop(suite)
        shutil.rmtree(self.path + '/' + suite)
        return self.suites
