import os
import datetime
from GeometrA.src.Report.ReportInfo import Info
from GeometrA.src.Report import ReportUI
from GeometrA.src.Controller.FileLoader import FileLoader
from GeometrA.src.Report.ReportStep import Step

PATH = lambda p: os.path.abspath(p)

class CaseReport:
    def __init__(self, title):
        self.htmlfile = ""
        self.day = ""
        self.time = ""
        self.title = title
        self.insert(ReportUI.getTitle(self.title))

    def start(self):
        self.info = Info()
        self.rstep = Step()

    def end(self, result, n):
        self.info.setStepCount(n)
        self.info.setEndTime()
        self.info.setResult(result)
        self.insert(self.info.report_info())
        self.insert(self.rstep.reportStep())

    def stepStart(self, step):
        self.rstep.stepBefore(step)

    def stepEnd(self, step, n):
        self.rstep.stepAfter()
        self.rstep.setStep(step, n)

    def createDir(self, filepath):
        ctime = str(datetime.datetime.now()).split(' ')
        date = ctime[0]
        self.time = ctime[1].split('.')[0].replace(':', '-')
        self.path = PATH(filepath + "/report/" + date)
        if not os.path.isdir(PATH(self.path)):
            os.makedirs(self.path)

    def exportHTML(self, path):
        self.filePath = str(path) + '/' + self.title + '.html'
        with open(self.filePath, 'w') as htmlReport:
            htmlReport.write(self.htmlfile)
        return self.filePath

    def insert(self, html):
        self.htmlfile = self.htmlfile + html
