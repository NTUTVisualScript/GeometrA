import json
import os
from tkinter import filedialog
from PIL import Image


import sys
sys.path.append('../TestCase')
sys.path.append('../GUI')
sys.path.append('../GUI/TestCase')
from TestCaseUI import TestCaseUI
from TestCase import TestCase
from TestStep import Step

class SaveFile:
    def __init__(self):
        self._filePath = ""
        self._folderPath = ""
        self._fileName = ""

    def saveButtonClick(self):
        self.saveFile()

    def saveFile(self):
        self.getFilePath()
        self.getFolderName()
        if self._filePath is None or self._filePath is "": return
        self.jsonEncoder()

    def getFilePath(self):
        _f = filedialog.asksaveasfilename(title="Save as...", filetypes=[("TestCase JSON Files", "*.json")])
        if not _f is None:
            self._filePath = _f
            self._fileName = _f.split('/').pop()

    def getFolderName(self):
        _fp = self._filePath
        self._folderPath = _fp.rstrip('test')

    def jsonEncoder(self):
        _dataDict = {}
        _stepList = TestCaseUI.getTestCaseUI().stepList
        for i in range(len(_stepList)-1):
            _data = {}
            act = _stepList[i].action.get()
            val = _stepList[i].value.get()
            _data["action"] = act
            _data["value"] = val
            # if val is :

            # elif val is str:
            #     pass
            _dataDict[str(i + 1)] = _data

        with open(self._filePath, 'w', encoding='utf-8') as fp:
            json.dump(_dataDict, fp, indent=2)

class LoadFile:
    def __init__(self):
        self._filePath = ""
        self._folderPath = ""
        self._fileName = ""
        self.case = None

    def loadButtonClick(self):
        self.loadFile()
        TestCaseUI.getTestCaseUI().reloadTestCaseUI(self.case)

    def loadFile(self):
        self.getFilePath()
        self.getFolderName()
        if self._filePath is None or self._filePath is "": return
        self.jsonDecoder()

    def getFilePath(self):
        _f = filedialog.askopenfile(title="Select File", filetypes=[("TestCase JSON Files", "*.json")])
        if _f is None:
            self._filePath = ""
        else:
            self._filePath = _f.name
            self._fileName = _f.name.split('/').pop()

    def getFolderName(self):
        _fp = self._filePath
        self._folderPath = _fp.rstrip(self._fileName)

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
