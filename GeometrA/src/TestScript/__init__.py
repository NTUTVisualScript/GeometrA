import json
from io import BytesIO
import base64
from PIL import Image, ImageTk

from GeometrA.src.TestScript.TestCase import TestCase
from GeometrA.src.TestScript.Executor import Executor
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

    def load(self, path):
        case = TestCase()
        self._caseList[path] = case
        path = path + '/testcase.json'
        with open(path, 'r') as f:
            case_data = json.loads(f.read())
        main_data = case_data['Main']
        for i in main_data:
            action = main_data[i]["Action"]
            from GeometrA.src import IMAGEACTIONLIST
            if action in IMAGEACTIONLIST:
                value = Image.open(BytesIO(base64.b64decode(main_data[i]["Value"].replace("data:image/png;base64,", ""))))
            else:
                value = main_data[i]["Value"]
            case.insert(act=action, val=value)

    def runAll(self):
        for caseName in self._caseList:
            exe = Executor(self._caseList[caseName])
            exe.runAll()
        return 'success'
