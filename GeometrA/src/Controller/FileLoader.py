import json
import os
from tkinter import filedialog
from PIL import Image
from GeometrA.src.TestScript.TestCase import TestCase
from GeometrA.src.TestScript.TestStep import Step

# class SaveFile:
#     def saveButtonClick(self, event=None):
#         from  GeometrA.src.GUI.TestCase.TestCaseUI import TestCaseUI
#         if TestCaseUI.getTestCaseUI().ctrl.save:
#             return
#         self.saveFile()
#
#     def saveAsButtonClick(self, event=None):
#         self._filePath = ''
#         self.saveButtonClick()
#
#     def saveFile(self):
#         try:
#             self.checkEntryValid()
#             if self._filePath == '':
#                 self.getSaveFilePath()
#             self.getFolderName()
#             if self._filePath == '': return
#             self.jsonEncoder()
#             from GeometrA.src.TestCase.TestCaseUI import TestCaseUI
#             TestCaseUI.getTestCaseUI().ctrl.caseSaved(True)
#         except Exception as step:
#             self._filePath = ''
#
#     def checkEntryValid(self):
#         from GeometrA.src.TestCase.TestCaseUI import TestCaseUI
#         for i in range(len(TestCaseUI.getTestCaseUI().stepList)):
#             value = TestCaseUI.getTestCaseUI().stepList[i].value
#             if str(value.__class__) == "<class 'TestCaseEntry.TestCaseValue'>":
#                 if TestCaseUI.getTestCaseUI().stepList[i].value['fg'] == 'red':
#                     raise Exception(int(i+1))
#             else:
#                 if TestCaseUI.getTestCaseUI().stepList[i].value.image == None:
#                     raise Exception(int(i+1))
#
#
#     def getSaveFilePath(self):
#         _f = filedialog.asksaveasfilename(title="Save as...", filetypes=[("TestCase JSON Files", "*.json")])
#         if not _f is '':
#             if '.json' not in _f:
#                 _f = _f + '.json'
#             self._filePath = _f
#             self._fileName = _f.split('/').pop().rstrip('.json')
#
#     def jsonEncoder(self):
#         from  GeometrA.src.GUI.TestCase.TestCaseUI import TestCaseUI
#         from  GeometrA.src.Controller.TreeController import Tree
#         _dataDict = {}
#         _case = TestCaseUI.getTestCaseUI().ctrl.case
#         for i in range(_case.getSize()):
#             _data = {}
#             act = _case.getSteps(i).getAction()
#             val = _case.getSteps(i).getValue()
#             _data['action'] = act
#             if (str(val.__class__) == "<class 'PIL.PngImagePlugin.PngImageFile'>") | \
#                 (str(val.__class__) == "<class 'PIL.Image.Image'>"):
#                 # Image path format: /*TestCaseName*_image/image_*StepNumber*.png
#                 _imgpath = self._fileName + "_image/image_" + str(i + 1) + ".png"
#                 if not os.path.isdir(self._folderPath + self._fileName + "_image"):
#                     os.makedirs(self._folderPath + self._fileName + "_image")
#                 val.save(self._folderPath + _imgpath)
#                 _data['value'] = None
#                 _data['image'] = _imgpath
#                 _data['nodePath'] = _case.getSteps(i).getNode()
#             else:
#                 _data['value'] = val
#                 _data['image'] = None
#                 _data['nodePath'] = None
#
#             _dataDict[str(i + 1)] = _data
#
#         with open(self._filePath, 'w', encoding='utf-8') as fp:
#             json.dump(_dataDict, fp, indent=2)

class LoadFile:
    # def loadButtonClick(self, event=None):
    #     from  GeometrA.src.GUI.TestCase.TestCaseUI import TestCaseUI
    #     self.loadFile()
    #     if self._filePath != '':
    #         self.modelConnect()
    #         TestCaseUI.getTestCaseUI().reloadTestCaseUI()
    #         TestCaseUI.getTestCaseUI().ctrl.caseSaved(True)

    def loadFile(self, path):
        # from GeometrA.src.GUI.TestCase.TestCaseUI import TestCaseUI
        try:
            # if
            self._filePath = path
            self.getFileName()
            # else:
            #     self.getLoadFilePath()
            self.getFolderName()
            if self._filePath is None or self._filePath is "": return
            self.jsonDecoder()
        except Exception as e:
            print(e)
            self._filePath = ''
            TestCaseUI.getTestCaseUI().ctrl.clearTestCase()


    # def getLoadFilePath(self):
    #     self._filePath = ""
    #     _f = filedialog.askopenfile(title="Select File", filetypes=[("TestCase JSON Files", "*.json")])
    #     if _f is None: return
    #     self._filePath = _f.name
    #     self.getFileName()
    #     return self._filePath

    def jsonDecoder(self):
        with open(self._filePath, 'r') as f:
            dataDic = json.load(f)
        self.case = TestCase()

        for i in range(len(dataDic)):
            data = dataDic[str(i + 1)]

            act = data['action']
            val = data['value']

            node = None
            if val is None:
                val = Image.open(self._folderPath + data['image'])
                node = data['nodePath']

            step = Step(act, val, node)
            self.case.insert(step=step)

    def modelConnect(self):
        from GeometrA.src.GUI.TestCase.TestCaseUI import TestCaseUI
        from GeometrA.src.TestScript.Executor import Executor
        TestCaseUI.getTestCaseUI().ctrl.case = self.case
        TestCaseUI.getTestCaseUI().ctrl.exe = Executor(self.case)

    def getTestCase(self):
        return self.case

class FileLoader(LoadFile):
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
        return self._fileName

    def getFolderName(self):
        _fp = self._filePath
        self._folderPath = _fp.rstrip(self._fileName + '.json')
        return self._folderPath
