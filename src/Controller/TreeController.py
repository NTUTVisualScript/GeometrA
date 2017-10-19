'''
    Tree

    Here is for us to get xml tree information of the objects on the current screen of android devices.
    Then, display those information on TreeUI to let user could get the information they need.

    User can get test case value as simple as click the node they need which is displayed in TreeUI, and it'll show on focusing TestCase.
'''

from PIL import Image as IMG, ImageTk
import xml.etree.cElementTree as ET
from adbRobot import ADBRobot
from GUI.TreeUI import TreeUI
from ScreenShotController import GetScreenShot
from tkinter import *
from ScreenshotUI import ScreenshotUI
from TestCaseUI import TestCaseUI as TCUI

class Tree(TreeUI):
    __single = None
    def __init__(self, parent=None):
        if Tree.__single:
            raise Tree.__single

        super().__init__(parent)    # To construct the UI part of tree.
        self.xmlPath = ""
        self.nodes = []
        self.screenImage = None

    def getTree(parent=None):
        if not Tree.__single:
            Tree.__single = Tree(parent)
        return Tree.__single

    def reload(self):
        self.clearTree()

        self.exportXML()
        self.treeInfo(self.xmlFile)

    def exportXML(self):
        self.xmlPath = ADBRobot().get_uiautomator_dump()
        self.xmlFile = ET.ElementTree(file=self.xmlPath)

    def clearTree(self):
        for row in self.get_children():
            self.delete(row)

    def clearImage(self, event=None):
        if self.screenImage:
            self.screenImage.destroy()

    def treeInfo(self, info, id=''):
        for elem in info.findall('node'):
            if elem is None: return
            child_id = self.insert(id, 'end', elem, \
                                    text='(' + str(elem.get('index')) + ') ' + str(elem.get('class')) + '  ', \
                                    values=( str(elem.get('text')), str(elem.get('bounds')) ), open=True)
            self.nodes.append(child_id)

            self.treeInfo(elem, child_id)

    def selectNode(self, event):
        self.selected = self.selection()[0]
        path = []
        self.nodePath(self.selected, path)
        self.selectImage()
        TCUI.getTestCaseUI().ctrl.setStep(TCUI.getTestCaseUI().focus, self.image, path)
        TCUI.getTestCaseUI().reloadTestCaseUI()

    def selectImage(self):
        itemValue = self.item(self.selected, 'value')[1]

        # self.select = self.nodes.index(self.selected)
        coor = self.splitBounds(itemValue)
        self.nodeImage(self.coorThumb(coor))

        # Used for the data to store in back end
        path = ('./screenshot_pic/tmp.png')
        self.image = IMG.open(path).crop(coor)

    def nodeImage(self, coor):
        if self.screenImage:
            self.screenImage.destroy()
        path = ('./screenshot_pic/tmp.png')
        img = IMG.open(path)
        img.thumbnail((GetScreenShot.x, GetScreenShot.y))
        img = img.crop(coor)
        img = ImageTk.PhotoImage(img)


        self.screenImage = Canvas(ScreenshotUI.getScreenshotUI(), height=coor[3] - coor[1], width=coor[2] - coor[0])
        self.screenImage.configure(borderwidth = -3)
        self.screenImage.place( x = coor[0], y = coor[1])

        self.screenImage.create_image(0, 0, anchor=NW, image=img)
        self.screenImage.image = img
        self.screenImage.create_rectangle(0, 0, coor[2]-coor[0]-3, coor[3]-coor[1]-3, outline='red', width=5)


    def splitBounds(self, bounds):
        bounds = bounds.replace('][', ',')
        bounds = bounds.replace('[', '')
        bounds = bounds.replace(']', '')

        vals = bounds.split(',')

        self.left = float(vals[0])
        self.top = float(vals[1])
        self.right = float(vals[2])
        self.bottom = float(vals[3])

        return (self.left, self.top, self.right, self.bottom)

    def coorThumb(self, coor):
        result = ()
        for i in coor:
            result = result + (i/GetScreenShot.multiple, )
        return result

    def nodePath(self, item, path):
        itemValue = []
        itemValue.append(self.item(item, "text"))
        value = self.item(item, "value")
        itemValue.append(value[0])
        path.append(itemValue)

        if self.parent(item):
            self.nodePath(self.parent(item), path)
        else:
            return path
