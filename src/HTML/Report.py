import os
import datetime
from ReportInfo import Info

class Report:
    def __init__(self):
        self.htmlfile = ""
        self.day = ""
        self.time = ""
        self.info = Info()

    def createDir(self, filepath):
        ctime = str(datetime.datetime.now()).split(' ')
        date = ctime[0]
        self.time = ctime[1].split('.')[0].replace(':', '-')
        self.path = PATH(filepath + "/report/" + date)
        if not os.path.isdir(PATH(self.path)):
            os.makedirs(self.path)
            self.htmlfile = ""

    def exportHTML(self):
        with open(str(self.path) + '/' + self.time + '.html', 'w') as htmlReport:
            htmlReport.write(self.htmlfile)
        return str(self.path) + '/' + self.time + '.html'

    def insert(self, html):
        self.htmlfile = self.htmlfile + html
