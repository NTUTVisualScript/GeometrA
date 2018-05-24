from GeometrA.src.ADB.adbRobot import ADBRobot
import xml.etree.cElementTree as ET

class Node:
    def __init__(self):
        self.xml = []

    def data(self):
        return self.xml

    def export(self):
        self.xmlPath = ADBRobot().get_uiautomator_dump()
        self.xmlFile = ET.ElementTree(file=self.xmlPath)
        self.treeInfo(self.xmlFile, self.xml)

    def treeInfo(self, info, xml):
        for elem in info.findall('node'):
            if elem is None: return
            _index = str(elem.get('index'))
            _name = str(elem.get('text'))
            _text = str(elem.get('class'))
            _bounds = str(elem.get('bounds'))
            data = {}
            data['text'] = _text
            data['data'] = {}
            data['data']['name'] = _name
            data['data']['index'] = _index
            data['data']['bounds'] = _bounds
            data['children'] = []
            xml.append(data)
            self.treeInfo(elem, data['children'])
