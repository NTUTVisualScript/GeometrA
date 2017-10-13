import xml.etree.cElementTree as ET
from adbRobot import ADBRobot
from GUI.TreeUI import TreeUI
from uiautomator import device as d

class Tree(TreeUI):
    __single = None
    def __init__(self, parent=None):
        if Tree.__single:
            raise Tree.__single

        super().__init__(parent)
        self.xmlPath = ""
        self.node = []
        self.maxRank = 0

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
        # self.xmlPath = './dumpXML/uidump.xml'
        # d.dump(self.xmlPath)
        self.xmlFile = ET.ElementTree(file=self.xmlPath)

    def clearTree(self):
        for row in self.get_children():
            self.delete(row)

    def treeInfo(self, info, id='', rank=0):
        for elem in info.findall('node'):
            if elem is None: return
            child_id = self.insert(id, 'end', elem, \
                                    text='(' + str(elem.get('index')) + ') ' + str(elem.get('class')) + '  ', \
                                    values=( str(elem.get('text')), str(elem.get('bounds')) ), open=True)
            # self.node.append(child_id)
            if self.maxRank < rank:
                self.maxRank = rank
            self.treeInfo(elem, child_id, rank+1)
