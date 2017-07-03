import os

from HTML.report_time import HTMLtime

PATH = lambda p: os.path.abspath(p)



class Report:
    __single = None

    def __init__(self, parent = None):
        if Report.__single:
            raise Report.__single
            Message.__single = self
        self.htmlfile = ""
        self.day = ""
        self.time = ""

    def getReport():
        if not Report.__single:
            Report.__single = Report()
        return Report.__single



    def creatReport(self, filepath):
        dirtime = HTMLtime()
        day = dirtime.get_dirday()
        time = dirtime.get_dirtime()
        self.path = PATH(filepath+"/report/"+ day+"/"+time)
        if not os.path.isdir(PATH(self.path)):
            os.makedirs(self.path)
            self.htmlfile = ""

    def outputHTML(self):
        with open(str(self.path+'/report.html'), 'w') as htmlReport:
            htmlReport.write(self.htmlfile)
        return str(self.path+'/report.html')

    def insert(self, testcaseAction):
        self.htmlfile = self.htmlfile + testcaseAction
