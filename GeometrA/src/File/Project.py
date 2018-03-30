from GeometrA.src.File.TestSuite import TestSuite
import os, shutil
import json

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
        if not origin in self.suites:
            raise KeyError(origin + " not in the project")
        if new in self.suites:
            raise Exception('Suite already exists')
        os.rename(self.path + '/' + origin, self.path + '/' + new)
        self.suites[new] = self.suites.pop(origin)
        self.suites[new].path = self.path + '/' + new
        self.updateRecord()

    def add(self, suite, case = None):
        if not case:
            if os.path.isdir(self.path + '/' + suite):
                raise Exception('Suite: "' + suite + '" is already exists!')
            self.suites[suite] = TestSuite([], self.path + '/' + suite)
            os.mkdir(self.path + '/' + suite)
        else:
            self.suites[suite].insert(case)
        self.updateRecord()

    def updateRecord(self):
        d = self.getJSON()
        projectName = self.path.split('/')[-1]
        data = [ projectName, { projectName: d } ]
        with open (self.path + '/' + projectName + '.json', 'w') as f:
            f.write(json.dumps(data))

    def delete(self, suite):
        self.suites.pop(suite)
        shutil.rmtree(self.path + '/' + suite)
        return self.suites

    def getJSON(self):
        result = {}
        for suite in self.suites:
            result[suite] = self.suites[suite].cases
        return result

    def getTreeJSON(self):
        result = []
        for suite in self.suites:
            d = {}
            d["text"] = suite
            d["children"] = self.suites[suite].getTreeJSON()
            result.append(d)
        return result
