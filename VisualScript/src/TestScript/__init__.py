from VisualScript.src.TestScript.TestCase import TestCase
class TestScript:
    def __init__(self):
        self._caseList = {}

    def add(self, name, case):
        self._caseList[name] = case

    def size(self):
        return len(self._caseList)

    def getCase(self, name):
        return self._caseList[name]

    def modified(self, name, data):
        case = TestCase()
        for i in range(len(data)):
            act = data[i]['act']
            val = data[i]['val']
            case.insert(act=act, val=val)

        self._caseList[name] = case
