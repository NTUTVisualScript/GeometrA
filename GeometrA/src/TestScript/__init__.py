import json
from io import BytesIO
import base64
from PIL import Image, ImageTk

from GeometrA.src.TestScript.TestCase import TestCase
from GeometrA.src.TestScript.Executor import Executor
from GeometrA.src.Report import CaseReport
from GeometrA.src.Report import Report

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
        reportIndex = Report()
        reportList = []
        for casePath in self._caseList:
            suitePath = casePath[:casePath.rfind('/')]
            projectPath = suitePath[:suitePath.rfind('/')]
            exe = Executor(self._caseList[casePath])
            result, report = self.execute(exe, casePath)
            reportList.append(report)
            reportIndex.addCase(casePath, result)
        reportPath = reportIndex.generate()
        for report in reportList:
            report.exportHTML(reportPath)
        return json.dumps({'state': 'success', 'reportPath': reportPath + '/index.html'})

    def execute(self, exe, path):
        name = path.split('/')[-1]
        report = CaseReport(name)
        size = exe.case.getSize()
        i = 0
        status = ''
        report.start()
        while i < size:
            step = exe.case.getSteps(i)
            report.stepStart(step)
            status = exe.execute(i)
            report.stepEnd(step, i)
            loop = 'Loop'
            if step.getAction() == loop:
                i = exe.loopEnd(i)
            f = 'Failed'
            e = 'Error'
            if (status == f) or status == e:
                break;
            i = i+1
        report.end(status, size)
        return (status, report)
