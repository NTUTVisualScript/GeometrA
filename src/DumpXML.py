import os
from tkinter import *
from tkinter import ttk
import xml.etree.cElementTree as ET
from adb_roboot import ADBRobot

ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(ROOT_DIR, "dumpXML")

dumpXMLfilePath = None

def IMG_PATH(name):
    return os.path.join(RESOURCES_DIR, name)

def Dump_UI():
    global dumpXMLfilePath
    robot = ADBRobot()
    dumpXMLfilePath = IMG_PATH(robot.get_uiautomator_dump())
    print(dumpXMLfilePath)
    return dumpXMLfilePath

class dumpXML(Frame):

    def XMLTreeUI(self):
        self.treeview = ttk.Treeview(self.master)
        self.treeview["columns"] = ("one")
        self.treeview.column("one", width=150)
        self.treeview.heading("one", text="Bounds")
        self.treeview.column('#0', stretch=YES, minwidth=0, width=500)
        self.treeview.grid(column=25 + 1, row=3, rowspan=15, columnspan=20, sticky='WE')

        self.Yvertscroll = Scrollbar(self.master, orient=VERTICAL)
        self.Yvertscroll.config(command=self.treeview.yview)
        self.Yvertscroll.grid(column=25 + 22, row=3, rowspan=15, columnspan=1, sticky='NS')

        self.Xvertscroll = Scrollbar(self.master, orient=HORIZONTAL)
        self.Xvertscroll.config(command=self.treeview.xview)
        self.Xvertscroll.grid(column=25 + 1, row=18, rowspan=1, columnspan=20, sticky='WE')

        self.treeview.config(yscrollcommand=self.Yvertscroll.set)
        self.treeview.config(xscrollcommand=self.Xvertscroll.set)
        self.treeview.bind("<<TreeviewSelect>>", self.on_tree_select)


    def Tree_infomation(self):
        self.XMLFile = ET.ElementTree(file=Dump_UI())
        self.tree_info("", self.XMLFile)

    def tree_info(self,id , treeinfo):
        for elem in treeinfo.findall('node'):
            if elem is None: return
            id_child = self.treeview.insert(id, "end", elem , text="(" + str(elem.get('index')) + ") "
                                                                   + str(elem.get('class')) + "  " + str(elem.get('text'))
                                                                   + "  ",  values=(str(elem.get('bounds'))) , open=True)
            self.tree_info(id_child, elem)

    def clear_XML_Tree(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)

    def on_tree_select(self, event):   #取得所選擇的List  value  中的Bounds
        for item in self.treeview.selection():
            item_value = self.treeview.item(item, "value")

        bounds = item_value[0].split('[')
        right_bounds = bounds[1].split(']')
        left_bounds = bounds[2].split(']')

        right_top = right_bounds[0].split(',')
        left_bottom = left_bounds[0].split(',')

        rigth = int(right_top[0])
        top = int(right_top[1])
        left = int(left_bottom[0])
        bottom = int(left_bottom[1])
        print(str(rigth) + "\n" + str(top) + "\n" + str(left) + "\n" + str(bottom) + "\n" )

        #
        # self.resetScreenShot()
        # w = event.widget
        # index = int(w.curselection()[0])
        # value = w.get(index)
        # mylist = value.split('[')
        # right = str(mylist[1]).split(']')
        # right = str(right[0]).split(',')
        #
        # left = str(mylist[2]).split(']')
        # left = str(left[0]).split(',')
        #
        # self.left = float(right[0]) / self.resize
        # self.top = float(right[1]) / self.resize
        # self.right = float(left[0]) / self.resize
        # self.bottom = float(left[1]) / self.resize
        #
        # self.cropImage(self.left , self.top ,
        #                self.right , self.bottom)
        #
        # self.drawRectangle(self.left , self.top ,
        #                self.right , self.bottom)