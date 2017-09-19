import json
from tkinter import filedialog
from PIL import Image, ImageTk


import sys
sys.path.append('../TestCase')
sys.path.append('../GUI')
sys.path.append('../GUI/TestCase')
from TestCaseUI import TestCaseUI
from TestCase import TestCase
from TestStep import Step
import StepOperate

class FileLoader():
    def SaveFile():
        pass

    def LoadFile():
        pass
        # _path = LoadFile.getFolderName
        # LoadFile()


class SaveFile():
    pass

class LoadFile():
    def __init__(self):
        self._filePath = ""
        self._folderPath = ""

    def loadButtonClick(self):
        self.loadPath()
        TestCaseUI.getTestCaseUI().reloadTestCaseUI(self.case)

    def loadPath(self):
        self.getFilePath()
        self.getFolderName()
        if self._filePath is None or self._filePath is "": return
        self.jsonDecoder()

    def getFilePath(self):
        _f = filedialog.askopenfile(title="Select File", filetypes=[("TestCase JSON Files", "*.json")])
        if not _f is None:
            self._filePath = _f.name

    def getFolderName(self):
        _fp = self._filePath
        self._folderPath = _fp.rstrip('testcase.json')

    def jsonDecoder(self):
        with open(self._filePath, 'r') as f:
            dataDic = json.load(f)
        self.case = TestCase()

        for i in range(len(dataDic)):
            data = dataDic[str(i+1)]

            act = data['action']
            val = data['value']
            if val == None:
                val = Image.open(self._folderPath + data['image'])

            step = Step(act, val)
            self.case.insert(step=step)

    def getTestCase(self):
        return self.case
