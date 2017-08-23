import json
import tkinter.filedialog
from PIL import Image, ImageTk

import sys
sys.path.append('../TestCase')
from TestCase import TestCase
from TestStep import Step

class FileLoader():
    def __init__(self, path):
        self.folderPath = path
        self.folderName = str(path.split('/').pop())
        self.jsonDecoder()

    def loadPath(self):
        dirPath = tkinter.filedialog.askdirectory()

        if dirPath is None or dirPath == '': return

        self.folderPath = dirPath
        self.folderName = str(dirPath.split('/').pop())

        return dirPath

    def getFolderName(self):
        return self.folderName

    def jsonDecoder(self):
        with open(self.folderPath + '/TestCase.json', 'r') as f:
            dataDic = json.load(f)

        self.case = TestCase()

        for i in range(len(dataDic)):
            data = dataDic[str(i+1)]

            act = data['action']
            val = data['value']
            if val == None:
                val =Image.open(self.folderPath + data['image'])
            step = Step()
            step.setAction(act)
            step.setValue(val)
            self.case.insert(i, step)

    def getTestCase(self):
        return self.case
