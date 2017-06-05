from tkinter import *
from tkinter import ttk
import os
from adb_roboot import ADBRobot
import xml.etree.cElementTree as ET
from PIL import Image, ImageTk
from DumpScreenShot import DumpScreenshot

ROOT_DIR = os.path.dirname(__file__)
RESOURCES_XML = os.path.join(ROOT_DIR, "dumpXML")

def XML_PATH(name):
    return os.path.join(RESOURCES_XML, name)

def Dump_Info():
    global dumpXMLfilePath
    robot = ADBRobot()
    dumpXMLfilePath = XML_PATH(robot.get_uiautomator_dump())
    print(dumpXMLfilePath)
    return dumpXMLfilePath

class DumpXML(ttk.Treeview):
    __single = None

    def __init__(self, parent = None, *args, **kwargs):
        ttk.Treeview.__init__(self, parent, *args, **kwargs)
        if DumpXML.__single:
            raise DumpXML.__single
            DumpXML.__single = self

        self.tree_obj_image_list = []
        self.tree_obj_list = []

        self.column('#0',text = "Class", stretch=YES, minwidth=0, width=350)
        self["columns"] = ("one", "two")
        self.column("one", width=150)
        self.heading("one", text="Text")
        self.column("two", width=150)
        self.heading("two", text="Bounds")

        self.bind("<ButtonRelease-1>", self.on_tree_select)


    def getDumpXML(parent):
        if not DumpXML.__single:
            DumpXML.__single = DumpXML(parent)
        return DumpXML.__single

    def Tree_infomation(self):
        self.XMLFile = ET.ElementTree(file=Dump_Info())

        self.screenshotImage = DumpScreenshot.getDumpscreenshot(self)

        if self.tree_obj_image_list != None:
            del self.tree_obj_image_list[:]
            del self.tree_obj_list[:]
        self.rankMax = 0
        self.tree_info("", 0, self.XMLFile)
        # self.Set_Tree_image_place()

    def tree_info(self, id, rank, treeinfo):
        for elem in treeinfo.findall('node'):
            if elem is None: return
            # print(elem.attrib)
            id_child = self.treeview.insert(id, "end", elem, text="(" + str(elem.get('index')) + ") "
                                                                  + str(elem.get('class')) + "  "
                                            , values=(str(elem.get('text')), str(elem.get('bounds'))), open=True)
            self.tree_obj_image(rank, str(elem.get('bounds')))
            self.tree_obj_list.append(id_child)
            if self.rankMax <= rank:
                self.rankMax = rank
            self.tree_info(id_child, rank + 1, elem)

    def root_to_node_path(self, item, path):
        item_value = []
        item_value.append(self.item(item, "text"))
        value = self.item(item, "value")
        item_value.append(value[0])
        path.append(item_value)

        if self.parent(item):
            self.root_to_node_path(self.parent(item), path)
        else:
            return path

    def bounds_split(self,obj_bounds):
        bounds = obj_bounds.split('[')
        right_bounds = bounds[1].split(']')
        left_bounds = bounds[2].split(']')

        right_top = right_bounds[0].split(',')
        left_bottom = left_bounds[0].split(',')

        left = int(right_top[0])
        top = int(right_top[1])
        right = int(left_bottom[0])
        bottom = int(left_bottom[1])
        return left, top, right, bottom

    def on_tree_select(self, event):   #取得所選擇的item value  中的Bounds
        for item in self.selection():
            item_value = self.item(item, "value")

        self.left, self.top, self.right, self.bottom = self.bounds_split(item_value[1])


        #self.resetScreenShot()

        # if self.focus != None:
        #     if self.actioncombolist[self.focus].get() == 'Click' or self.actioncombolist[self.focus].get() == 'Assert Exist' or self.actioncombolist[self.focus].get() == 'Assert Not Exist':
        #         self.screenshotImage.cropImage(self.focus, self.left, self.top, self.right, self.bottom)
        #
        #     if self.actioncombolist[self.focus].get() == 'Drag':
        #         text = "x=" + str( int((self.left * self.multiple + self.left * self.multiple) / 2) ) +\
        #                ",y=" + str( int((self.right * self.multiple + self.left * self.bottom) / 2) )
        #         self.valuelist[self.focus].delete(0, 'end')
        #         self.valuelist[self.focus].insert('end', text)

    def tree_obj_image(self, rank, obj_bounds):

        obj_image_info = []
        left, top, right, bottom = self.bounds_split(obj_bounds)
        left, top, right, bottom = left / self.multiple, top / self.multiple, right / self.multiple, bottom / self.multiple

        img = self.screenshotImage.photo.crop((left, top, right, bottom))
        image = ImageTk.PhotoImage(img)

        obj_image = Canvas(self.screenshotImage, height=bottom - top, width=right - left)
        obj_image.configure(borderwidth=-3)
        obj_image.place(x=left, y=top)

        obj_image.create_image(0, 0, anchor=NW, image=image)
        obj_image.image = image

        obj_image.bind("<Button-1>",
                       lambda event, i=len(self.tree_obj_image_list): self.screenshotImage.clickdown(event, i))  # clickdown
        obj_image.bind("<ButtonRelease-1>",
                       lambda event, i=len(self.tree_obj_image_list): self.screenshotImage.clickup(event, i))  # clickup
        obj_image.bind("<Motion>",
                       lambda event, i=len(self.tree_obj_image_list): self.screenshotImage.motion(event, i))  # get mouse coordination
        obj_image.bind("<Enter>", lambda event, i=len(self.tree_obj_image_list): self.screenshotImage.mouseEnter(event, i, right - left,
                                                                                                 bottom - top))
        obj_image.bind("<Leave>", lambda event, i=len(self.tree_obj_image_list): self.screenshotImage.mouseLeave(event, i))
        obj_image.bind("<B1-Motion>",
                       lambda event, i=len(self.tree_obj_image_list): self.screenshotImage.mouseDragged(event, i))  # 滑鼠拖拉動作

        obj_image_info.append(rank)
        obj_image_info.append(obj_image)
        obj_image_info.append(left)
        obj_image_info.append(top)
        print(obj_image_info)
        self.tree_obj_image_list.append(obj_image_info)

    def clear_XML_Tree(self):
        for row in self.get_children():
            self.delete(row)