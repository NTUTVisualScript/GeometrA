import json
from tkinter import filedialog
from PIL import Image

import sys
sys.path.append('../TestCase')
from TestCase import TestCase
from TestStep import Step

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
        self._filePath = None
        self._folderPath = None
        # self.folderName = str(path.split('/').pop())
        # self.jsonDecoder()

    def loadPath(self):
        self.getFilePath()
        self.getFolderName()
        if self._filePath is None or self._filePath == '': return

        self.jsonDecoder()


        return dirPath.name

    def getFilePath(self):
        _f = filedialog.askopenfile(title="Select File", filetypes=[("TestCase JSON Files", "*.json")])
        self._filePath = _f.name

    def getFolderName(self):
        _fp = self._filePath
        print(_fp.split('/'))
        self._folderPath = str(_fp.split('/').pop())

    def jsonDecoder(self):
        with open(self._filePath, 'r') as f:
            dataDic = json.load(f)

        self.case = TestCase()

        for i in range(len(dataDic)):
            data = dataDic[str(i+1)]

            act = data['action']
            val = data['value']
            if val == None:
                val =Image.open(self._filePath + data['image'])
            step = Step(act, val)
            self.case.insert(step=step)

    def getTestCase(self):
        return self.case
