import datetime
from jinja2 import Environment, PackageLoader, select_autoescape
from GeometrA.src.ADB.adbRobot import ADBRobot
import os

class Report:
    def __init__(self):
        self.env = Environment(
            loader=PackageLoader('GeometrA', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.template = self.env.get_template('Report/report.html')
        self.setSerialNumber()
        self.setDisplay()
        self.count = 0
        self.projects = {}

    def setSerialNumber(self):
        self.serialNumber = ADBRobot().get_devices()

    def setDisplay(self):
        self.display = ADBRobot().get_device_size()

    def getReport(self):
        self.time = str(datetime.datetime.now()).split('.')[0]
        return self.template.render( date=self.time, serialNumber=self.serialNumber,
            display=self.display, count=self.count, projects=self.projects)

    def addCase(self, path, status):
        self.path = path
        temp = path.split('/')
        project = temp[-3]
        suite = temp[-2]
        case = temp[-1]
        if (project in self.projects):
            if (suite in self.projects[project]):
                self.projects[project][suite][case] = status
            else:
                self.projects[project][suite] = { case: status }
        else:
            self.projects[project] = { suite: { case: status } }

    def getReportPath(self):
        suitePath = self.path[:self.path.rfind('/')]
        projectPath = suitePath[:suitePath.rfind('/')]
        return projectPath + '/report'

    def generate(self):
        report = self.getReport()
        reportPath = self.getReportPath()
        if not os.path.isdir(reportPath):
            os.mkdir(reportPath)
        date, time = self.time.split(' ')
        reportDate = reportPath + '/' + date
        if not os.path.isdir(reportDate):
            os.mkdir(reportDate)
        time = time.replace(":", "-")
        reportTime = reportDate + '/' + time
        os.mkdir(reportTime)
        with open(reportTime + '/index.html', 'w') as f:
            f.write(report)
