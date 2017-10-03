import os
from HTML.report_time import HTMLtime

class TestReport:
    def __init__(self, parent = None):
        # if Report.__single:
        #     raise Report.__single
        #     Report.__single = self
        self.dirpath = ""
        self.htmlfile = ""
        self.day = ""
        self.time = ""

    def createTestReport(self):
        from FileLoader import FileLoader
        folderPath = FileLoader.getFileLoader()._folderPath
        fileName = FileLoader.getFileLoader()._fileName
        if FileLoader.getFileLoader()._folderPath != "":
            self.dirpath = folderPath + '/' + fileName + '_report'
            if not os.path.isdir(self.dirpath):
                os.makedirs(self.dirpath)
        else:
            raise Exception
