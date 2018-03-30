import os
import datetime
from GeometrA.src.HTML.ReportInfo import Info
import GeometrA.src.HTML.ReportUI
from GeometrA.src.Controller.FileLoader import FileLoader
from GeometrA.src.HTML.ReportStep import Step
from GeometrA.src.GUI.MessageUI import Message

PATH = lambda p: os.path.abspath(p)

class Report:
    def __init__(self):
        self.htmlfile = ""
        self.day = ""
        self.time = ""
        title = FileLoader.getFileLoader().getFileName()
        self.insert(HTML.ReportUI.getTitle(title))

    def start(self):
        self.info = Info()
        self.rstep = Step()

    def end(self, result, n):
        self.info.setStepCount(n)
        self.info.setEndTime()
        self.info.setResult(result)
        self.insert(self.info.report_info())
        self.insert(self.rstep.reportStep())

        path = FileLoader.getFileLoader().getFolderName()
        self.createDir(path)
        self.exportHTML()
        Message.getMessage().report(self.filePath)

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

    def exportHTML(self):
        with open(str(self.path) + '/' + self.time + '.html', 'w') as htmlReport:
            htmlReport.write(self.htmlfile)
        self.filePath = str(self.path) + '/' + self.time + '.html'
        return self.filePath

    def insert(self, html):
        self.htmlfile = self.htmlfile + html
