from tkinter import *
from adb_roboot import ADBRobot
from PIL import Image, ImageTk
import os

ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(ROOT_DIR, "screenshot_pic")

filePath = None

def IMG_PATH(name):
    return os.path.join(RESOURCES_DIR, name)

def Get_PhoneScreen():
    global filePath
    robot = ADBRobot()
    filePath = IMG_PATH(robot.screenshot())
    print(filePath)
    return filePath

class DumpScreenshot(Canvas):
    __single = None

    def __init__(self, parent=None, *args, **kwargs):
        Canvas.__init__(self, parent, *args, **kwargs)
        if DumpScreenshot.__single:
            raise DumpScreenshot.__single
            DumpScreenshot.__single = self

        self.configure(borderwidth=-1)
        self.multiple = 1
        self.focusOBJImage = None
        self.Drag_image = None

    def getDumpscreenshot(parent):
        if not DumpScreenshot.__single:
            DumpScreenshot.__single = DumpScreenshot(parent)
        return DumpScreenshot.__single

    def getScreenShot(self):
        self.delete("all")
        self.photo = Image.open(Get_PhoneScreen())
        self.photo_width, self.photo_height = self.photo.size
        print(str(self.photo_width) + " , " + str(self.photo_height))
        self.photo.thumbnail((450, 800))
        self.width, self.height = self.photo.size
        self.multiple = self.photo_width / self.width
        print(str(self.multiple))
        self.screenshot_photo = ImageTk.PhotoImage(self.photo)
        self.create_image(0, 0, anchor=NW)
        self.image = self.screenshot_photo

    def resetScreenShot(self):
        self.delete("all")
        self.create_image(0, 0, anchor=NW, image=self.screenshot_photo)

    def cropImage(self,line, left, top, right, bottom):
        photo = Image.open(filePath)
        self.cropped = photo.crop((left , top , right  , bottom ))

        self.valueImagelist[line] = self.cropped
        # print("valueImagelist = " + str(line))
        photo2 = Image.open(filePath)
        img = photo2.crop((left, top, right, bottom))
        img.thumbnail((100, 100))
        image = ImageTk.PhotoImage(img)

        self.TestcaseImage(line, image)

    def drawRectangle(self, line, left, top, right, bottom):
        self.xmltree.tree_obj_image_list[line][1].create_rectangle(left  , top  , right  , bottom  , outline='red', width=2)

    def clickdown(self, event, line):
        if filePath is None: return
        self.resetScreenShot()

        x = int(self.xmltree.tree_obj_image_list[line][1].place_info().get('x'))
        y = int(self.xmltree.tree_obj_image_list[line][1].place_info().get('y'))
        w = self.xmltree.tree_obj_image_list[line][1].winfo_width()
        h = self.xmltree.tree_obj_image_list[line][1].winfo_height()
        self.clickstartX = event.x + x
        self.clickstartY = event.y + y

        node_path = []
        self.xmltree.root_to_node_path(self.xmltree.xmltree.tree_obj_list[line], node_path)
        node_path.reverse()
        #
        #
        # print("len(node_path) = ",len(node_path))
        # for i in range(len(node_path)):
        #     print(node_path[i])

        # if self.focus != None:
        #     if self.actioncombolist[self.focus].get() == 'Click'or self.actioncombolist[self.focus].get() == 'Assert Exist'or self.actioncombolist[self.focus].get() == 'Assert Not Exist':
        #         self.valuelist[self.focus].delete(0, 'end')
        #         for item in self.treeview.selection():
        #             value = self.treeview.item(item, "value")
        #         bounds = value[1]
        #         left, top, right, bottom = self.bounds_split(bounds)
        #         self.cropImage(self.focus, left, top, right, bottom)
        #         self.node_path_list[self.focus] = node_path

    def clickup(self, event, line):
        if filePath is None: return

        x = int(self.tree_obj_image_list[line][1].place_info().get('x'))
        y = int(self.tree_obj_image_list[line][1].place_info().get('y'))
        self.clickendX = event.x + x
        self.clickendY = event.y + y
        self.left, self.right = sorted([self.clickendX, self.clickstartX])
        self.top, self.bottom = sorted([self.clickstartY, self.clickendY])

        # if (self.right - self.left) > 5  or (self.bottom - self.top) > 5 or (self.right - self.left) < -5 or (self.right - self.left) < -5:
        #     if self.focus != None:
        #         if self.actioncombolist[self.focus].get() == 'Click' or self.actioncombolist[self.focus].get() == 'Assert Exist' or self.actioncombolist[self.focus].get() =='Assert Not Exist':
        #             self.valuelist[self.focus].delete(0, 'end')
        #             self.cropImage(self.focus, self.left * self.multiple, self.top * self.multiple, self.right * self.multiple, self.bottom * self.multiple)
        #
        #         elif self.actioncombolist[self.focus].get() == 'Drag':
        #             text = "start x=" + str(int(self.clickstartX * self.multiple)) + ", y=" + str(int(self.clickstartY * self.multiple)) + " , " +\
        #                    "end x=" + str(int(self.clickendX * self.multiple)) + ", y=" + str(int(self.clickendY * self.multiple))
        #             self.valuelist[self.focus].delete(0, 'end')
        #             self.valuelist[self.focus].insert('end', text)

    def motion(self,event, line):
        x = int(self.tree_obj_image_list[line][1].place_info().get('x'))
        y = int(self.tree_obj_image_list[line][1].place_info().get('y'))
        #self.mousePosition.set("Mouse in window [ " + str(int((x + event.x) * self.multiple)) + ", " + str(int((y + event.y) * self.multiple)) + " ]")

    def mouseEnter(self, event, line, w, h):
        self.focusOBJImage = self.xmltree.tree_obj_image_list[line][1].image
        self.xmltree.tree_obj_image_list[line][1].create_rectangle(0, 0 , w-3 , h -3, outline='red', width=5)
        text = [""]
        text.insert(0, self.xmltree.tree_obj_list[line])
        self.xmltree.selection_set(text)
        self.xmltree.yview_moveto(line/len(self.tree_obj_list))
        #print(self.treeview.parent(self.tree_obj_list[line]))

    def mouseLeave(self, event, line):
        self.xmltree.tree_obj_image_list[line][1].delete("all")
        self.xmltree.tree_obj_image_list[line][1].create_image(0, 0, anchor=NW, image=self.focusOBJImage)
        self.xmltree.tree_obj_image_list[line][1].image = self.focusOBJImage

    def mouseDragged(self, event, line):
        if filePath is None: return
        self.xmltree.tree_obj_image_list[line][1].delete("all")
        self.xmltree.tree_obj_image_list[line][1].create_image(0, 0, anchor=NW, image=self.focusOBJImage)
        self.xmltree.tree_obj_image_list[line][1].image = self.focusOBJImage

        x = int(self.xmltree.tree_obj_image_list[line][1].place_info().get('x'))
        y = int(self.xmltree.tree_obj_image_list[line][1].place_info().get('y'))


        if event.x < 0 :
            event.x = 0
        if event.y < 0 :
            event.y = 0
        if event.x > self.screenshot_photo.width():
            event.x = self.screenshot_photo.width()
        if event.y > self.screenshot_photo.height():
            event.y = self.screenshot_photo.height()

        #self.mousePosition.set("Rectangle at [ " + str(self.clickstartX * self.multiple ) + ", " + str(self.clickstartY * self.multiple) + " To " + str((event.x + x) * self.multiple) + ", " + str((event.y + y) * self.multiple) + " ]")
        #if self.actioncombolist[self.focus].get() == 'Click' or self.actioncombolist[self.focus].get() == 'Assert Exist':
        self.drawRectangle(line, self.clickstartX - x, self.clickstartY - y, event.x, event.y)

    def Dragdown(self, event):
        self.clickstartX = event.x
        self.clickstartY = event.y

    def Dragup(self, event):
        self.clickendX = event.x
        self.clickendY = event.y
        self.left, self.right = sorted([self.clickendX, self.clickstartX])
        self.top, self.bottom = sorted([self.clickstartY, self.clickendY])

        # if self.left != self.right or self.top != self.bottom:
        #         if self.actioncombolist[self.focus].get() == 'Drag':
        #             text = "start x=" + str(int(self.clickstartX * self.multiple)) + ", y=" + str(int(self.clickstartY * self.multiple)) + " , " +\
        #                    "end x=" + str(int(self.clickendX * self.multiple)) + ", y=" + str(int(self.clickendY * self.multiple))
        #             self.valuelist[self.focus].delete(0, 'end')
        #             self.valuelist[self.focus].insert('end', text)

    def Dragmotion(self,event):
        print("Mouse in window [ " + str(int((event.x) * self.multiple)) + ", " + str(int((event.y) * self.multiple)) + " ]")
        #self.mousePosition.set("Mouse in window [ " + str(int((event.x) * self.multiple)) + ", " + str(int((event.y) * self.multiple)) + " ]")

    def DragEnter(self, event):
        self.focusOBJImage = self.Drag_image.image

    def Dragged(self, event):
        self.Drag_image.delete("all")
        self.Drag_image.create_image(0, 0, anchor=NW, image=self.focusOBJImage)
        self.Drag_image.image = self.focusOBJImage

        #self.mousePosition.set("Rectangle at [ " + str(self.clickstartX * self.multiple ) + ", " + str(self.clickstartY * self.multiple) + " To " + str((event.x) * self.multiple) + ", " + str((event.y) * self.multiple) + " ]")
        self.Drag_image.create_line(self.clickstartX, self.clickstartY, event.x, event.y, fill="red", width=2)