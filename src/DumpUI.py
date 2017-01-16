import os
from tkinter import *
import xml.etree.cElementTree as ET
from adb_roboot import ADBRobot

ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources/taipeibus")

filePath = None
dumpXMLfilePath = None

def IMG_PATH(name):
    return os.path.join(RESOURCES_DIR, name)

def Dump_UI():
    global dumpXMLfilePath
    robot = ADBRobot()
    dumpXMLfilePath = IMG_PATH(robot.get_uiautomator_dump())
    print(dumpXMLfilePath)
    return dumpXMLfilePath

class dumpUI:

    def onselect(self, event):   #取得所選擇的List  value  中的Bounds
        self.resetScreenShot()
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        #print('You selected item %d: "%s"' % (index, value))
        mylist = value.split('[')
        right = str(mylist[1]).split(']')
        right = str(right[0]).split(',')

        left = str(mylist[2]).split(']')
        left = str(left[0]).split(',')

        self.left = float(right[0]) / self.resize
        self.top = float(right[1]) / self.resize
        self.right = float(left[0]) / self.resize
        self.bottom = float(left[1]) / self.resize

        self.cropImage(self.left , self.top ,
                       self.right , self.bottom)

        self.drawRectangle(self.left , self.top ,
                       self.right , self.bottom)

    def getXMLTree(self, tree):
        tree = ET.ElementTree(file = Dump_UI())
        self.tree_bounds(tree, 0)
        return tree
        # self.tree = dom.parse(file=Dump_UI())
        # self.add_element_to_treestore(self.tree.childNodes , None)

    def clear_XML_Tree(self, tree):
        tree.delete( 0 , END )

    def tree_bounds(self, tree, num):
        for elem in tree.findall('node'):
            st = ""
            for n in range(num):
                print("\t", end="")  # 不換行
                st = st + "          "
            print(elem.get('bounds'))
            strstr = st + "(" + str(elem.get('index')) + ") " + str(elem.get('class')) + "  " + str \
                (elem.get('text')) + "  " + str(elem.get('bounds')) + "\n"
            tree.insert(END, strstr)
            self.tree_bounds(elem, num + 1)