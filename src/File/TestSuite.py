import os, shutil

from File.TestCase import TestCase

class TestSuite:
    def __init__(self, caseList, path):
        self.path = path
        self.check(caseList)
        self.cases = []
        self.insert(caseList)

    def insert(self, cases):
        if str(cases.__class__) == "<class 'list'>":
            for case in cases:
                if case == '':
                    raise Exception('Empty case name in the list!')
                if self.cases.count(case) != 0:
                    raise Exception('Case exist!')
                self.cases.append(case)
        elif str(cases.__class__) == "<class 'str'>" :
            if cases == '':
                raise Exception('Empty case name!')
            if self.cases.count(cases) != 0:
                raise Exception('Case exist!')

            self.cases.append(cases)
        else:
            raise Exception('Invalid case name!')

    def delete(self, case):
        n = self.cases.index(case)
        self.cases.pop(n)
        shutil.rmtree(self.path + '/' + case)
        return self.cases

    def rename(self, origin, new):
        if new in self.cases:
            raise Exception('Case already exists')
        n = self.cases.index(origin)
        self.cases[n] = new
        os.rename(self.path + '/' + origin, self.path + '/' + new)

    def check(self, cases):
        notExist = []
        for case in cases:
            path = self.path + '/' + case
            if not os.path.isdir(path):
                notExist.append(case)
        for case in notExist:
            cases.remove(case)

    def getTreeJSON(self):
        result = []
        for i in self.cases:
            d = {}
            d["text"] = i
            result.append(d)
        return result
