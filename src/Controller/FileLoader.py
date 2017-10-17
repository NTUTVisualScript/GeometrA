import json
import os
from tkinter import filedialog
from PIL import Image
from TestCase import TestCase
from TestStep import Step
from MessageUI import Message
from GUI.DialogueForm import  DialogueForm


class SaveFile:
    def saveButtonClick(self, event=None):
        self.saveFile()
        Message.getMessage().fileSaved(self._filePath)

    def saveFile(self):
        try:
            self.checkEntryValid()
            self.getSaveFilePath()
            self.getFolderName()
            if self._filePath == '': return
            self.jsonEncoder()
            from TestCaseUI import TestCaseUI
            TestCaseUI.getTestCaseUI().ctrl.caseSaved(True)
        except Exception as step:
            self._filePath = ''
            DialogueForm.Messagebox("Insert Error!","The Value of Step "+str(step)+" is wrong!")

    def checkEntryValid(self):
        from TestCaseUI import TestCaseUI
        for i in range(len(TestCaseUI.getTestCaseUI().stepList)):
            value = TestCaseUI.getTestCaseUI().stepList[i].value
            if str(value.__class__) == "<class 'TestCaseEntry.TestCaseValue'>":
                if TestCaseUI.getTestCaseUI().stepList[i].value['fg'] == 'red':
                    raise Exception(int(i+1))
            else:
                if TestCaseUI.getTestCaseUI().stepList[i].value.image == None:
                    raise Exception(int(i+1))


    def getSaveFilePath(self):
        _f = filedialog.asksaveasfilename(title="Save as...", filetypes=[("TestCase JSON Files", "*.json")])
        if not _f is '':
            if '.json' not in _f:
                _f = _f + '.json'
            self._filePath = _f
            self._fileName = _f.split('/').pop().rstrip('.json')

    def jsonEncoder(self):
        from TestCaseUI import TestCaseUI
        _dataDict = {}
        _case = TestCaseUI.getTestCaseUI().ctrl.case
        for i in range(_case.getSize()):
            _data = {}
            act = _case.getSteps(i).getAction()
            _data['action'] = act
            if (str(_case.getSteps(i).getValue().__class__) == "<class 'PIL.PngImagePlugin.PngImageFile'>") | \
                (str(_case.getSteps(i).getValue().__class__) == "<class 'PIL.Image.Image'>"):
                # Image path format: /*TestCaseName*_image/image_*StepNumber*.png
                _imgpath = self._fileName + "_image/image_" + str(i + 1) + ".png"
                if not os.path.isdir(self._folderPath + self._fileName + "_image"):
                    os.makedirs(self._folderPath + self._fileName + "_image")
                _case.getSteps(i).getValue().save(self._folderPath + _imgpath)
                _data['value'] = None
                _data['image'] = _imgpath
            else:
                val = _case.getSteps(i).getValue()
                _data['value'] = val
                _data['image'] = None

            _dataDict[str(i + 1)] = _data

        with open(self._filePath, 'w', encoding='utf-8') as fp:
            json.dump(_dataDict, fp, indent=2)

class LoadFile:
    def loadButtonClick(self, event=None):
        from TestCaseUI import TestCaseUI
        self.loadFile()
        self.modelConnect()
        if self._filePath != '':
            TestCaseUI.getTestCaseUI().reloadTestCaseUI()
            TestCaseUI.getTestCaseUI().ctrl.caseSaved(True)
        Message.getMessage().fileLoaded(self._filePath)

    def loadFile(self, path=None):
        from GUI.TestCase.TestCaseUI import TestCaseUI
        try:
            if path:
                self._filePath = path
                self.getFileName()
            else:
                self.getLoadFilePath()
            self.getFolderName()
            if self._filePath is None or self._filePath is "": return
            self.jsonDecoder()
        except Exception as e:
            print(e)
            # DialogueForm.Messagebox("Load Test Case Error!","The file '"+ self._filePath.split('/')[-1] + "' is invalid format.")
            self._filePath = ''
            TestCaseUI.getTestCaseUI().ctrl.clearTestCase()


    def getLoadFilePath(self):
        self._filePath = ""
        _f = filedialog.askopenfile(title="Select File", filetypes=[("TestCase JSON Files", "*.json")])
        if _f is None: return
        self._filePath = _f.name
        self.getFileName()

    def jsonDecoder(self):
        with open(self._filePath, 'r') as f:
            dataDic = json.load(f)
        self.case = TestCase()

        for i in range(len(dataDic)):
            data = dataDic[str(i + 1)]

            act = data['action']
            val = data['value']
            if val is None:
                val = Image.open(self._folderPath + data['image'])

            step = Step(act, val)
            self.case.insert(step=step)

    def modelConnect(self):
        from TestCaseUI import TestCaseUI
        from Executor import Executor
        TestCaseUI.getTestCaseUI().ctrl.case = self.case
        TestCaseUI.getTestCaseUI().ctrl.exe = Executor(self.case)

    def getTestCase(self):
        return self.case

class FileLoader(SaveFile, LoadFile):
    __single = None

    def __init__(self):
        if FileLoader.__single:
            raise FileLoader.__single
        FileLoader.__single = self
        self._filePath = ""
        self._folderPath = ""
        self._fileName = ""
        self.case = None

    def getFileLoader():
        if FileLoader.__single is None:
            FileLoader.__single = FileLoader()
        return FileLoader.__single

    def getFileName(self):
        self._fileName = self._filePath.split('/').pop().rstrip('.json')

    def getFolderName(self):
        _fp = self._filePath
        self._folderPath = _fp.rstrip(self._fileName + '.json')
        return self._folderPath
