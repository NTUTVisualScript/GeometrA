import json
import tkinter.filedialog
import sys
sys.path.append('../TestCase')
from TestCase import TestCase

class FileLoader():
    def __init__(self):
        self.folderPath = ''
        self.folderName = ''
        self.case = None

    def loadPath(self):
        dirPath = tkinter.filedialog.askdirectory()

        if dirPath is None or dirPath == '': return

        self.folderPath = dirPath
        self.folderName = str(dirPath.split('/').pop())

        return dirPath

    def getFolderName(self):
        return self.folderName

    def jsonDecoder(self, dirPath):
        with open(dirPath + '/TestCase.json', 'r') as f:
            dataDic = json.load(f)

        self.case = TestCase(len(dataDic))

        for i in range(self.case.getSize()):
            data = dataDic[str(i+1)]

            act = data['action']
            val = data['value']

            self.case.setAction(i, act)
            self.case.setValue(i, val)

    def getTestCase(self):
        return self.case
