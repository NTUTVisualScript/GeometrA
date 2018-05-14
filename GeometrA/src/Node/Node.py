from GeometrA.src.ADB.adbRobot import ADBRobot
import xml.etree.cElementTree as ET

class Node:
    def __init__(self):
        self.xml = []

    def data(self):
        return self.xml[0]

    def export(self):
        # self.xmlPath = ADBRobot().get_uiautomator_dump()
        self.xmlPath = './dumpXML/uidump.xml'
        self.xmlFile = ET.ElementTree(file=self.xmlPath)
        self.treeInfo(self.xmlFile, self.xml)

    def treeInfo(self, info, xml):
        for elem in info.findall('node'):
            if elem is None: return
            # child_id = self.insert(id, 'end', elem, \
            #                         text='(' + str(elem.get('index')) + ') ' + str(elem.get('class')) + '  ', \
            #                         values=( str(elem.get('text')), str(elem.get('bounds')) ), open=True)
            _index = str(elem.get('index'))
            _class = str(elem.get('class'))
            _text = str(elem.get('text'))
            data = {}
            data['index'] = _index
            data['class'] = _class
            data['name'] = _text
            data['children'] = []
            xml.append(data)
            self.treeInfo(elem, data['children'])
