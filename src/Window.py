import os
import threading
import time
import math
import xml.etree.cElementTree as ET
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from PIL import Image, ImageTk

import CommandManager
from CheckADBConnection import checkADB_Connection
from HTML.devices_infomation import HTML_divices_Info
from HTML.report_time import HTMLtime
from HTML.title import HtmlHead
from LoadFile import LoadFile
from MessageUI import Message
from SaveFile import SaveFile
from SaveIMG import saveImg
from TestCaseActionCombobox import TestCaseAction
from TestCaseEntry import TestCaseValue
from GUI.OldScreenShotUI import ScreenshotUI
from TestReport import Report
from Viewtest import TestAdepter
from adbRobot import ADBRobot
from HTML.step import HtmlTestStep

ROOT_DIR = os.path.dirname(__file__)
PIC_LOADING = os.path.join(ROOT_DIR, "img")

filePath = None
dumpXMLfilePath = None

def Dump_UI():
    global dumpXMLfilePath
    robot = ADBRobot()
    dumpXMLfilePath = robot.get_uiautomator_dump()
    print(dumpXMLfilePath)
    return dumpXMLfilePath

def Get_PhoneScreen():
    global filePath
    robot = ADBRobot()
    filePath = robot.screenshot()
    print(filePath)
    return filePath

class View(Frame, threading.Thread):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.minsize(width=1470, height=840)
        self.master = master
        self.setUI()

    def setUI(self):
        self.focus = None
        self.focusOBJImage = None
        self.Drag_image = None
        self.update_image = None
        self.tree_obj_image_list = []
        self.tree_obj_list = []
        self.dirpath = ""
        self.dirName = ""
        self.select_node = None
        self.select_image = None
        self.checkADB = checkADB_Connection()
        self.cmd = CommandManager
        self.savecropImg = saveImg()
        self.XMLTreeUI()
        self.MessageUI()
        #self.SaveIMGButton()
        self.RunButton()
        self.getmouseEvent()

    def MenuBar(self):
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)

        filemenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Save  Test Case as...", command = self.SaveButtonClick)
        filemenu.add_command(label="Open  Test Case as...", command = self.LoadButtonClick)

        actionmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Action", menu=actionmenu)
        actionmenu.add_command(label="Undo", command=self.undo)
        actionmenu.add_command(label="Redo", command=self.redo)
        # self.bind("<Control-z>", self.undo)
        # self.bind("<Control-y>", self.redo)

    def MessageUI(self):
        self.messagetitle = Label(self.master, text="Message Log", font=("Helvetica",16))
        self.messagetitle.place(x=1150, y=0)
        self.message = Message.getMessage(self.master)
        #self.message.config(state=DISABLED)
        self.message.place(x=1150, y=30)

    def ScreenShotUI(self):
        self.screenshot = ScreenshotUI.getScreenShotUI(self.master)

    def getScreenShot(self):
        self.screenshot.delete("all")
        self.LoadingFile()
        self.photo = Image.open(Get_PhoneScreen())
        self.photo_width, self.photo_height = self.photo.size
        print(str(self.photo_width) + " , " + str(self.photo_height))
        self.photo.thumbnail((450, 800))
        self.width, self.height = self.photo.size
        self.multiple = self.photo_width / self.width
        print(str(self.multiple))
        self.screenshot_photo = ImageTk.PhotoImage(self.photo)
        self.message.InsertText("Loading finish\n")
        self.screenshot.create_image(0, 0, anchor=NW)
        self.screenshot.image = self.screenshot_photo

    def LoadingFile(self):
        self.message.InsertText("Loading files...\nPlease wait...\n")
        if self.tree_obj_image_list != None:
            for i in range(len(self.tree_obj_image_list)):
                self.tree_obj_image_list[i][1].place_forget()
        #
        # loadimgpath = os.path.join(PIC_LOADING, "loading.gif")
        # print(loadimgpath)
        # pilImage = Image.open(loadimgpath)
        # self.loading = ImageTk.PhotoImage(pilImage)
        # self.screenshot.create_image(0, 0, anchor=CENTER)
        # self.screenshot.image = self.loading

    def getImgPath(self):
        return filePath

    def getCropRange(self):
        return self.left, self.top, self.right, self.bottom, self.multiple

    def resetScreenShot(self):
        self.screenshot.delete("all")
        self.screenshot.create_image(0, 0, anchor=NW, image=self.screenshot_photo)

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
        self.tree_obj_image_list[line][1].create_rectangle(left  , top  , right  , bottom  , outline='red', width=2)

    def getmouseEvent(self):
        self.mousePosition = StringVar()  # displays mouse position
        self.mousePosition.set("Mouse outside window")
        self.positionLabel = Label(self.master, textvariable=self.mousePosition)
        self.positionLabel.place(x = 820, y = 270)

    def root_to_node_path(self, item, path):
        item_value = []
        item_value.append(self.treeview.item(item, "text"))
        value = self.treeview.item(item, "value")
        item_value.append(value[0])
        path.append(item_value)

        if self.treeview.parent(item):
            self.root_to_node_path(self.treeview.parent(item), path)
        else:
            return path

    def clickdown(self, event, line):
        if filePath is None: return
        self.resetScreenShot()

        x = int(self.tree_obj_image_list[line][1].place_info().get('x'))
        y = int(self.tree_obj_image_list[line][1].place_info().get('y'))
        w = self.tree_obj_image_list[line][1].winfo_width()
        h = self.tree_obj_image_list[line][1].winfo_height()
        self.clickstartX = event.x + x
        self.clickstartY = event.y + y

        node_path = []
        self.root_to_node_path(self.tree_obj_list[line], node_path)
        node_path.reverse()
        #
        #
        # print("len(node_path) = ",len(node_path))
        # for i in range(len(node_path)):
        #     print(node_path[i])
        print(line)
        if self.focus != None:
            self.add_changes(self.focus, "", self.actionlist[self.focus], self.valuelist[self.focus], self.valueImagelist[self.focus], self.node_path_list[self.focus])

            if self.actioncombolist[self.focus].get() == 'Click'or self.actioncombolist[self.focus].get() == 'Assert Exist'or self.actioncombolist[self.focus].get() == 'Assert Not Exist':
                self.valuelist[self.focus].delete(0, 'end')
                for item in self.treeview.selection():
                    value = self.treeview.item(item, "value")
                bounds = value[1]
                left, top, right, bottom = self.bounds_split(bounds)
                self.cropImage(self.focus, left, top, right, bottom)
                self.node_path_list[self.focus] = node_path

    def clickup(self, event, line):
        if filePath is None: return

        x = int(self.tree_obj_image_list[line][1].place_info().get('x'))
        y = int(self.tree_obj_image_list[line][1].place_info().get('y'))
        self.clickendX = event.x + x
        self.clickendY = event.y + y
        self.left, self.right = sorted([self.clickendX, self.clickstartX])
        self.top, self.bottom = sorted([self.clickstartY, self.clickendY])

        if (self.right - self.left) > 5  or (self.bottom - self.top) > 5 or (self.right - self.left) < -5 or (self.right - self.left) < -5:
            if self.focus != None:
                self.add_changes(line, "", self.actionlist[line], self.valuelist[line], self.valueImagelist[line],
                                 self.node_path_list[line])
                if self.actioncombolist[self.focus].get() == 'Click' or self.actioncombolist[self.focus].get() == 'Assert Exist' or self.actioncombolist[self.focus].get() =='Assert Not Exist':
                    self.valuelist[self.focus].delete(0, 'end')
                    self.cropImage(self.focus, self.left * self.multiple, self.top * self.multiple, self.right * self.multiple, self.bottom * self.multiple)

                elif self.actioncombolist[self.focus].get() == 'Swipe':
                    text = "start x=" + str(int(self.clickstartX * self.multiple)) + ", y=" + str(int(self.clickstartY * self.multiple)) + " , " +\
                           "end x=" + str(int(self.clickendX * self.multiple)) + ", y=" + str(int(self.clickendY * self.multiple))
                    self.valuelist[self.focus].delete(0, 'end')
                    self.valuelist[self.focus].insert('end', text)

    def motion(self,event, line):
        x = int(self.tree_obj_image_list[line][1].place_info().get('x'))
        y = int(self.tree_obj_image_list[line][1].place_info().get('y'))
        self.mousePosition.set("Mouse in window [ " + str(int((x + event.x) * self.multiple)) + ", " + str(int((y + event.y) * self.multiple)) + " ]")

    def mouseEnter(self, event, line, w, h):
        if self.select_node!= None:
            self.tree_obj_image_list[self.select_node][1].delete("all")
            self.tree_obj_image_list[self.select_node][1].create_image(0, 0, anchor=NW, image=self.select_image)
            self.tree_obj_image_list[self.select_node][1].image = self.select_image

        self.focusOBJImage = self.tree_obj_image_list[line][1].image
        self.tree_obj_image_list[line][1].create_rectangle(0, 0 , w-3 , h -3, outline='red', width=5)
        text = [""]
        text.insert(0, self.tree_obj_list[line])
        self.treeview.selection_set(text)
        self.treeview.yview_moveto(line/len(self.tree_obj_list))
        #print(self.treeview.parent(self.tree_obj_list[line]))

    def mouseLeave(self, event, line):
        self.tree_obj_image_list[line][1].delete("all")
        self.tree_obj_image_list[line][1].create_image(0, 0, anchor=NW, image=self.focusOBJImage)
        self.tree_obj_image_list[line][1].image = self.focusOBJImage

    def mouseDragged(self, event, line):
        if filePath is None: return
        self.tree_obj_image_list[line][1].delete("all")
        self.tree_obj_image_list[line][1].create_image(0, 0, anchor=NW, image=self.focusOBJImage)
        self.tree_obj_image_list[line][1].image = self.focusOBJImage

        x = int(self.tree_obj_image_list[line][1].place_info().get('x'))
        y = int(self.tree_obj_image_list[line][1].place_info().get('y'))


        if event.x < 0 :
            event.x = 0
        if event.y < 0 :
            event.y = 0
        if event.x > self.screenshot_photo.width():
            event.x = self.screenshot_photo.width()
        if event.y > self.screenshot_photo.height():
            event.y = self.screenshot_photo.height()

        self.mousePosition.set("Rectangle at [ " + str(self.clickstartX * self.multiple ) + ", " + str(self.clickstartY * self.multiple) + " To " + str((event.x + x) * self.multiple) + ", " + str((event.y + y) * self.multiple) + " ]")
        #if self.actioncombolist[self.focus].get() == 'Click' or self.actioncombolist[self.focus].get() == 'Assert Exist':
        self.drawRectangle(line, self.clickstartX - x, self.clickstartY - y, event.x, event.y)

    def XMLTreeUI(self):
        self.Yvertscroll = Scrollbar(self.master, orient=VERTICAL)

        self.Xvertscroll = Scrollbar(self.master, orient=HORIZONTAL)

        self.treeview = ttk.Treeview(self.master,yscrollcommand=self.Yvertscroll.set , xscrollcommand=self.Xvertscroll.set)
        self.treeview.column('#0', stretch=YES, minwidth=0, width=350)
        self.treeview.place( x = 460, y = 30)
        self.treeview["columns"] = ("one", "two")
        self.treeview.column("one", width=150)
        self.treeview.heading("one", text="Text")
        self.treeview.column("two", width=150)
        self.treeview.heading("two", text="Bounding Box")

        self.Yvertscroll.config(command=self.treeview.yview)
        self.Xvertscroll.config(command=self.treeview.xview)

        self.treeview.bind("<ButtonRelease-1>", self.on_tree_select_node)

    def Tree_infomation(self):
        # self.message.InsertText("Analysing files...\n")
        # self.XMLFile = ET.ElementTree(file=Dump_UI())

        if self.tree_obj_image_list != None:
            del self.tree_obj_image_list[:]
            del self.tree_obj_list[:]

        self.rankMax = 0
        self.tree_info("", 0, self.XMLFile)
        self.message.InsertText("Analysing finish\n")
        #self.Set_Tree_image_place()

    def tree_info(self,id , rank, treeinfo):
        for elem in treeinfo.findall('node'):
            if elem is None: return
            #print(elem.attrib)
            id_child = self.treeview.insert(id, "end", elem , text="(" + str(elem.get('index')) + ") "
                                                                   + str(elem.get('class')) + "  "
                                                                   ,  values=( str(elem.get('text')),str(elem.get('bounds'))) , open=True)
            self.tree_obj_image(rank ,str(elem.get('bounds')))
            self.tree_obj_list.append(id_child)
            if self.rankMax <= rank:
                self.rankMax = rank
            self.tree_info(id_child, rank+1, elem)

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

    def tree_obj_image(self,rank , obj_bounds):

        obj_image_info = []
        left, top, right, bottom = self.bounds_split(obj_bounds)
        left, top, right, bottom = left/ self.multiple, top/ self.multiple, right/ self.multiple, bottom/ self.multiple

        img = self.photo.crop((left, top, right, bottom))
        image = ImageTk.PhotoImage(img)

        obj_image= Canvas(self.screenshot, height=bottom - top, width=right - left)
        obj_image.configure(borderwidth = -3)
        obj_image.place( x = left, y = top)

        obj_image.create_image(0, 0, anchor=NW, image=image)
        obj_image.image = image

        obj_image.bind("<Button-1>", lambda event, i=len(self.tree_obj_image_list) : self.clickdown(event, i))  # clickdown
        obj_image.bind("<ButtonRelease-1>", lambda event, i=len(self.tree_obj_image_list) : self.clickup(event, i))  # clickup
        obj_image.bind("<Motion>", lambda event, i=len(self.tree_obj_image_list) : self.motion(event, i))  # get mouse coordination
        obj_image.bind("<Enter>", lambda event, i=len(self.tree_obj_image_list): self.mouseEnter(event, i,right - left, bottom - top))
        obj_image.bind("<Leave>", lambda event, i=len(self.tree_obj_image_list) : self.mouseLeave(event, i))
        obj_image.bind("<B1-Motion>", lambda event, i=len(self.tree_obj_image_list) : self.mouseDragged(event, i))  # 滑鼠拖拉動作

        obj_image_info.append(rank)
        obj_image_info.append(obj_image)
        obj_image_info.append(left)
        obj_image_info.append(top)
        #print(obj_image_info)
        self.tree_obj_image_list.append(obj_image_info)

    def Set_Tree_image_place(self):
        for i in range(self.rankMax + 1):
            for j in range(len(self.tree_obj_image_list)):
                if int(self.tree_obj_image_list[j][0]) == i:
                    left = self.tree_obj_image_list[j][2]
                    top = self.tree_obj_image_list[j][3]
                    self.tree_obj_image_list[j][1].configure(borderwidth=-3)
                    self.tree_obj_image_list[j][1].place(x = left, y = top)
                    print("rank " , i, " x = ", left, " y = ",  top)

        print(self.rankMax)

    def clear_XML_Tree(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)

    def on_tree_select_node(self, event):   #取得所選擇的item value  中的Bounds
        if self.select_node!= None:
            self.tree_obj_image_list[self.select_node][1].delete("all")
            self.tree_obj_image_list[self.select_node][1].create_image(0, 0, anchor=NW, image=self.select_image)
            self.tree_obj_image_list[self.select_node][1].image = self.select_image

        for item in self.treeview.selection():
            node = item
            item_value = self.treeview.item(item, "value")

        self.select_node = self.tree_obj_list.index(node)

        self.left, self.top, self.right, self.bottom = self.bounds_split(item_value[1])

        left, top, right, bottom = self.left / self.multiple, self.top / self.multiple, self.right / self.multiple, self.bottom / self.multiple

        self.select_image = self.tree_obj_image_list[self.select_node][1].image
        self.tree_obj_image_list[self.select_node][1].create_rectangle(0, 0, right - left - 3, bottom - top - 3, outline='red', width=5)
        #self.mouseEnter(event, i,right - left,bottom - top)
        #print(str(self.left) + "\n" + str(self.top) + "\n" + str(self.right) + "\n" + str(self.bottom) + "\n" )
        self.resetScreenShot()
        #print(self.focus)
        if self.focus != None:
            if self.actioncombolist[self.focus].get() == 'Click' or self.actioncombolist[self.focus].get() == 'Assert Exist' or self.actioncombolist[self.focus].get() == 'Assert Not Exist':
                self.cropImage(self.focus, self.left, self.top, self.right, self.bottom)

            if self.actioncombolist[self.focus].get() == 'Swipe':
                text = "x=" + str( int((self.left * self.multiple + self.left * self.multiple) / 2) ) +\
                       ",y=" + str( int((self.right * self.multiple + self.left * self.bottom) / 2) )
                self.valuelist[self.focus].delete(0, 'end')
                self.valuelist[self.focus].insert('end', text)

    def formatButton(self):
        self.dumpUI = Button(self.master, command=self.formatButtonClick, text="Dump UI",width=15)
        self.dumpUI.place(x = 0, y = 3)

    def formatButtonClick(self, getdevices =None):
        self.focus = None
        self.select_node = None
        self.select_image = None
        if getdevices ==None:
            self.message.clear()
            if self.checkADB.check() == "Connect":
                threading.Thread(target=self.format).start()
        else:
            threading.Thread(target=self.format).start()

    def format(self):
        self.clear_XML_Tree()
        if self.Drag_image != None:
            self.Drag_image.place_forget()

        self.screenshot.remove_run_test_screenshot()
        self.dump_file()
        # threading.Thread(target=self.getScreenShot).start()
        #self.getScreenShot()
        time.sleep(1)
        self.Tree_infomation()
        #threading.Thread(target=self.Tree_infomation).start()

    def dump_file(self):
        threading.Thread(target=self.getScreenShot).start()
        self.dump_xml()

    def dump_xml(self):
        self.message.InsertText("Analysing files...\n")
        self.XMLFile = ET.ElementTree(file=Dump_UI())


    def SaveIMGButton(self):
        self.SaveIMG = Button(self.master, command=self.SaveIMGButtonClick, text="Crop Image",width=15)
        self.SaveIMG.place(x = 120, y = 3)

    def SaveIMGButtonClick(self):
        # if filePath is None: return
        # self.savecropImg.Save(filePath, self.getCropRange())
        for i  in range(len(self.valueImagelist)):
            if self.valueImagelist[i] != None:
                #print(i)
                self.valueImagelist[i].show()
                for n in range(len(self.node_path_list[i])):
                    print(self.node_path_list[i][n])

    def ShowimageButtonClick(self, line):
        self.valueImagelist[line].show()

    def RunButton(self):
        self.runbutton = Button(self.master, command=self.RunButtonClick, text="Run",width=15)
        self.runbutton.place(x = 460, y = 270)

    def ResetButton(self):
        self.runbutton = Button(self.master, command=self.ResetButtonClick, text="Reset Testcase", width=15)
        self.runbutton.place(x = 580, y = 270)

    def SaveButtonClick(self):
        Save_File = SaveFile()
        self.dirpath = Save_File.SaveTestCase(self.actioncombolist, self.valuelist, self.valueImagelist,self.node_path_list)

    def LoadButtonClick(self):
        Load_File = LoadFile()
        dirpath = Load_File.LoadTestCasePath()
        if  dirpath != None:
            self.dirpath = dirpath
            print("dirpath : ", dirpath)
            self.ResetButtonClick()
            self.dirName = Load_File.get_folderName()
            Load_File.Decoder_Json(self.dirpath)
            actioncombo_list, value_list, valueImage_list, nodepath_list = Load_File.get_Loading_Data()
            for i in range(len(actioncombo_list)):
                self.actioncombolist[i].set(str(actioncombo_list[i]))

                self.valuelist[i].delete(0, 'end')
                self.valuelist[i].insert('end', str(value_list[i]))

                self.node_path_list[i] = nodepath_list[i]
                if valueImage_list[i] != None:
                    self.valueImagelist[i] = valueImage_list[i]
                    width, height = valueImage_list[i].size
                    img = valueImage_list[i].crop((0, 0, width, height))
                    img.thumbnail((100, 100))
                    image = ImageTk.PhotoImage(img)
                    self.TestcaseImage(i,image)


    def ResetButtonClick(self):
        self.TestCaseFrame()
        self.select_node = None
        self.select_image = None

    def AddLineButtonClick(self,n, redoundo ):

        if redoundo ==False:
            self.add_changes( n, "add", self.actionlist[n], self.valuelist[n], self.valueImagelist[n],
                            self.node_path_list[n])

        self.line  = self.line + 1
        self.new_line(self.line)
        i= self.line

        self.valueImagelist.insert(n, None)
        self.node_path_list.insert(n, None)

        while i > n:
            getactionstr = self.actioncombolist[i-1].get()
            self.actioncombolist[i].set(str(getactionstr))
            self.actioncombolist[i-1].set('')
            self.actionlist[i] = self.actionlist[i-1]
            self.actionlist[i-1] = ""

            if str(type(self.valuelist[i-1])) != "<class 'TestCaseEntry.TestCaseValue'>":
                self.TestcaseImage(i, self.valuelist[i-1].image)
                self.TestcaseEntry(i-1)

            else:
                getvaluestr = self.valuelist[i-1].get()
                self.valuelist[i].delete(0, 'end')
                self.valuelist[i].insert('end', getvaluestr)
                self.valuelist[i - 1].delete(0, 'end')

            i=i-1


    def RemoveLineButtonClick(self, n, do):
        if do == False:
            self.add_changes(n, "remove", self.actionlist[n], self.valuelist[n], self.valueImagelist[n],
                            self.node_path_list[n])

        del self.valueImagelist[n]
        del self.node_path_list[n]
        i = n
        while i < self.line:
            getactionstr = self.actioncombolist[i + 1].get()
            self.actioncombolist[i].set(str(getactionstr))
            self.actionlist[i] = self.actionlist[i + 1]
            self.actionlist[i + 1] = ""

            if str(type(self.valuelist[i+1])) != "<class 'TestCaseEntry.TestCaseValue'>":
                self.TestcaseImage(i, self.valuelist[i+1].image)
                self.TestcaseEntry(i+1)

            else:
                self.TestcaseEntry(i)
                getvaluestr = self.valuelist[i+1].get()
                self.valuelist[i].delete(0, 'end')
                self.valuelist[i].insert('end', getvaluestr)
                self.valuelist[i+1].delete(0, 'end')

            i = i + 1

        self.lineStrlist[self.line].grid_remove()
        self.actioncombolist[self.line].grid_remove()
        self.valuelist[self.line].grid_remove()
        self.addlinelist[self.line].grid_remove()
        self.removelinelist[self.line].grid_remove()
        self.run_single_actionlist[self.line].grid_remove()

        self.lineStrlist.pop()
        self.actioncombolist.pop()
        self.valuelist.pop()
        self.addlinelist.pop()
        self.removelinelist.pop()
        self.run_single_actionlist.pop()
        self.line = self.line - 1

    def Run_single_actionButtonClick(self, n):
        self.focus = n
        threading.Thread(target=self.Run_SingleTestCase).start()

    def RunButtonClick(self):
        if self.dirpath !="":
            threading.Thread(target=self.Run_ALLTestCase).start()
        else:
            messagebox.showwarning('警告', "您的測試尚未存檔，請先進行儲存再執行!!")

    def Run_SingleTestCase(self):
        data = TestAdepter()
        self.message.clear()
        if self.checkADB.check() == "Connect":
            n = self.focus
            action = []
            value = []
            image = []
            path_list = []
            action.append(self.actioncombolist[n])
            value.append(self.valuelist[n])
            image.append(self.valueImagelist[n])
            path_list.append(self.node_path_list[n])
            check_data = data.set_data(action, value, image, path_list)
            if check_data:
                action, value, image, path_list = data.get_data()
                data.run_single(n, action, value, image, path_list)
            else:
                self.message.InsertText("The Test case have some problem, please check action " + str(n + 1) + " !\n")

            self.formatButtonClick("no")

    def Run_ALLTestCase(self):
        data = TestAdepter()

        self.message.clear()
        if self.checkADB.check() == "Connect":
            report = Report.getReport()
            head = HtmlHead()
            htmltime = HTMLtime()
            htmlstep = HtmlTestStep.getHtmlTestStep()
            htmlstep.clearstep()
            report.creatReport(self.dirpath)
            head.set_title(self.dirName)
            info = HTML_divices_Info()
            info.set_SerialNo(self.checkADB.get_SerialNo())
            w,h = self.checkADB.get_Display()
            info.set_Display(w,h)

            check_data = data.set_data(self.actioncombolist, self.valuelist, self.valueImagelist, self.node_path_list)

            if check_data:
                start = htmltime.get_time()
                info.set_start_time(start)
                status, count = data.run_all()
                info.set_Result(status)
                info.set_StepCount(count)
                end = htmltime.get_time()
                info.set_end_time(end)
                info.report_Info()
                htmlstep.report_step()
                reportpath = report.outputHTML()

            finish = "\nThe Test Case Finish!\n"
            self.message.InsertText(finish)
            self.message.InsertText("\nYou can see report on this path\n")
            self.message.HyperLink(reportpath)
            self.message.InsertText("\n\n")
            self.formatButtonClick("no")


    def undo(self):
        if len(self.testcase_undo) != 0:
            print("undo ",self.testcase_undo)
            testcase_line = self.testcase_undo.pop()
            line = testcase_line[0]

            if str(type(self.valuelist[line])) == "<class 'TestCaseEntry.TestCaseValue'>":
                add_redo = [line, "", self.actioncombolist[line].get(), self.valuelist[line].get(),
                            self.valueImagelist[line], self.node_path_list[line]]
            else:
                add_redo = [line, "", self.actioncombolist[line].get(), self.valuelist[line].image,
                            self.valueImagelist[line], self.node_path_list[line]]

            self.testcase_redo.append(add_redo)

            print(line)
            if testcase_line[1] == "remove":
                self.AddLineButtonClick(line, True)
                self.actioncombolist[line].set(testcase_line[2])
                self.actionlist[line] = testcase_line[2]
                print("undo ", testcase_line[2])
                if testcase_line[2] == "Click" or testcase_line[2] == "Assert Exist" or \
                     testcase_line[2] == "Assert Not Exist":
                    self.TestcaseImage(line, testcase_line[3])
                else:
                    self.TestcaseEntry(line)
                    self.valuelist[line].delete(0, END)
                    self.valuelist[line].insert(0, testcase_line[3])

            elif testcase_line[1] == "add":
                self.RemoveLineButtonClick(line, True)
            elif testcase_line[2] == "Click" or testcase_line[2] == "Assert Exist" or \
                            testcase_line[2] == "Assert Not Exist":
                self.actioncombolist[line].set(testcase_line[2])
                self.TestcaseImage(line, testcase_line[3])
            else:
                self.TestcaseEntry(line)
                self.actioncombolist[line].set(testcase_line[2])
                self.valuelist[line].delete(0, END)
                if testcase_line[3]!= None:
                   self.valuelist[line].insert(0, testcase_line[3])

            self.valueImagelist[line] = testcase_line[4]
            self.node_path_list[line] = testcase_line[5]

    def redo(self):
        if len(self.testcase_redo) != 0:
            print("redo ",self.testcase_redo)
            testcase_line = self.testcase_redo.pop()
            line = testcase_line[0]

            if str(type(self.valuelist[line])) == "<class 'TestCaseEntry.TestCaseValue'>":
                add_undo = [line, "", self.actioncombolist[line].get(), self.valuelist[line].get(), self.valueImagelist[line], self.node_path_list[line]]
            else:
                add_undo = [line, "", self.actioncombolist[line].get(), self.valuelist[line].image, self.valueImagelist[line], self.node_path_list[line]]

            self.testcase_undo.append(add_undo)

            self.actioncombolist[line].set(testcase_line[2])
            if testcase_line[1] == "remove":
                self.RemoveLineButtonClick(line, True)
            elif testcase_line[1] == "add":
                self.AddLineButtonClick(line, True)
            elif testcase_line[2] == "Click" or testcase_line[2] == "Assert Exist" or \
                            testcase_line[2] == "Assert Not Exist":
                self.TestcaseImage(line, testcase_line[3])
            else:
                self.TestcaseEntry(line)
                self.valuelist[line].delete(0, END)
                if testcase_line[3] != None:
                    self.valuelist[line].insert(0, testcase_line[3])

            self.valueImagelist[line] = testcase_line[4]
            self.node_path_list[line] = testcase_line[5]



    def add_changes(self, line, change, action, value, image, path):
        print(str(type(value)))
        if str(type(value)) == "<class 'TestCaseEntry.TestCaseValue'>":
            testcase_line = [line, change, action, value.get(), image, path]
        else:
            testcase_line = [line, change, action, value.image, image, path]

        print(action)
        self.testcase_undo.append(testcase_line)
        del self.testcase_redo[:]


    def TestCaseFrame(self):
        self.frameTwo = Frame(self.master, borderwidth =2 ,relief = 'sunken')
        self.frameTwo.place(x=460, y=300)

        self.canvas = Canvas(self.frameTwo)
        self.listFrame = Frame(self.canvas)

        self.scrollb = Scrollbar(self.frameTwo, orient="vertical", command=self.canvas.yview)
        self.scrollb.pack(side='right', fill='y')
        self.canvas['yscrollcommand'] = self.scrollb.set

        self.canvas.create_window((0, 0), window=self.listFrame, anchor='nw')
        self.listFrame.bind("<Configure>", self.AuxscrollFunction)
        self.scrollb.grid_forget()

        self.canvas.pack(side="left")

        self.lineStrlist = []
        self.addlinelist = []
        self.removelinelist = []
        self.run_single_actionlist = []
        self.actioncombolist = []
        self.actionlist = []
        self.valuelist = []
        self.showimagelist = []
        self.valueImagelist = []
        self.node_path_list = []

        self.testcase_undo = []
        self.testcase_redo = []

        n=0
        for self.line in range(50):
            self.new_line(n)
            n=n+1

        print("line = " + str(self.line))

    def AuxscrollFunction(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=650, height=525)

    def TestcaseImage(self,line, image = None):
        #print("image : ",line)
        values_image = Canvas(self.listFrame, bg = "#FFFFFF",height=100, width=100)
        values_image.create_image(0, 0, anchor=NW, image=image)
        values_image.bind("<Button-1>", lambda event, i=line: self.valueFocusIn(event, i))
        values_image.image = image
        self.valuelist[line].grid_remove()
        self.valuelist[line] = values_image
        self.valuelist[line].grid(row=line + 1, column=6, padx=(5, 0), pady=(5, 2.5))
        self.showimagelist[line].grid(row=line + 1, column=7, padx = ( 5, 0) , pady = ( 5 , 2.5))

    def TestcaseEntry(self, line):
        value = TestCaseValue(self.listFrame, width=35)
        value.bind("<FocusIn>", lambda event, i=line: self.valueFocusIn(event, i))
        self.valuelist[line].grid_remove()
        self.showimagelist[line].grid_remove()
        self.valuelist[line] = value
        self.valuelist[line].grid(row=line + 1, column=6, padx=(5, 0), pady=(5, 2.5))

    def new_line(self,n):
        action_value = StringVar()

        lineStr = Label(self.listFrame, text=str(n+1)+". ", width=3)
        self.lineStrlist.append(lineStr)
        addline = Button(self.listFrame, command=lambda :self.AddLineButtonClick(n, False), text="+", width=3)
        self.addlinelist.append(addline)

        removeline = Button(self.listFrame, command=lambda :self.RemoveLineButtonClick(n, False), text="-", width=3)
        self.removelinelist.append(removeline)

        run_single_action = Button(self.listFrame, command=lambda: self.Run_single_actionButtonClick(n), text="▶", width=3)
        self.run_single_actionlist.append(run_single_action)

        actioncombo = TestCaseAction(self.listFrame, textvariable=action_value, width=10, height=22,
                                   state='readonly')
        actioncombo.bind("<<ComboboxSelected>>", lambda event, i=n: self.ActionSelect(event, i))
        actioncombo.bind("<MouseWheel>", lambda event, i=n: self.ActionSelect(event, i))
        self.actioncombolist.append(actioncombo)

        value = TestCaseValue(self.listFrame,width=35)
        value.bind("<FocusIn>", lambda event, i=n: self.valueFocusIn(event, i))

        showimage = Button(self.listFrame, command=lambda: self.ShowimageButtonClick(n), text="show image", width=12)
        self.showimagelist.append(showimage)

        self.valuelist.append(value)
        self.valueImagelist.append(None)
        self.node_path_list.append(None)
        self.actionlist.append("")

        lineStr.grid(row = n+1 , column = 1 )
        addline.grid(row = n+1 , column = 2 )
        removeline.grid(row=n+1, column=3)
        run_single_action.grid(row=n+1, column=4)
        actioncombo.grid(row = n+1 , column = 5 , padx = ( 5 , 0 ) , pady = ( 5 , 2.5))
        value.grid(row = n+1 , column = 6 , padx = ( 5, 0) , pady = ( 5 , 2.5))

    def ActionSelect(self,event, n):
        self.focus = n
        #self.cmd.do(self.actioncombolist[n])
        print(self.actionlist[n])
        self.add_changes(n, "", self.actionlist[n], self.valuelist[n], self.valueImagelist[n], self.node_path_list[n])
        self.actionlist[n] = self.actioncombolist[n].get()
        self.valueImagelist[n] = None
        self.TestcaseEntry(n)
        self.Action_FocusIn()

    def valueFocusIn(self,event, n):
        self.focus = n
        if self.actioncombolist[self.focus].get() != 'TestCase':
            self.Action_FocusIn()

    def Action_FocusIn(self):
        if self.actioncombolist[self.focus].get() != 'Swipe':
            if self.Drag_image != None:
                self.Drag_image.place_forget()
                self.Drag_image = None

        if self.actioncombolist[self.focus].get() == 'Swipe':
            if filePath is None: return
            self.Drag_image = Canvas(self.screenshot, height=800, width=450)
            self.Drag_image.configure(borderwidth=-3)
            self.Drag_image.place(x=0, y=0)

            self.Drag_image.create_image(0, 0, anchor=NW, image=self.screenshot_photo)
            self.Drag_image.image = self.screenshot_photo
            self.Drag_image.bind("<Button-1>", self.Dragdown)  # clickdown
            self.Drag_image.bind("<ButtonRelease-1>", self.Dragup)  # clickup
            self.Drag_image.bind("<Motion>", self.Dragmotion)  # get mouse coordination
            self.Drag_image.bind("<Enter>", self.DragEnter)
            self.Drag_image.bind("<B1-Motion>", self.Dragged)  # 滑鼠拖拉動作

        elif self.actioncombolist[self.focus].get() == 'TestCase':
            openfile = LoadFile()
            path = openfile.LoadTestCasePath()
            print(path)
            if path is not None:
                if path !="":
                    self.valuelist[self.focus].delete(0, 'end')
                    self.valuelist[self.focus].insert('end', path)
        elif self.actioncombolist[self.focus].get() == 'Click' or self.actioncombolist[self.focus].get() == 'Assert Exist' or self.actioncombolist[self.focus].get() == 'Assert Not Exist':
            self.TestcaseImage(self.focus)

        else:
            if self.Drag_image != None:
                self.Drag_image.place_forget()
                self.Drag_image = None

    def Dragdown(self, event):
        self.clickstartX = event.x
        self.clickstartY = event.y

    def Dragup(self, event):
        self.clickendX = event.x
        self.clickendY = event.y
        self.left, self.right = sorted([self.clickendX, self.clickstartX])
        self.top, self.bottom = sorted([self.clickstartY, self.clickendY])

        if self.left != self.right or self.top != self.bottom:
                if self.actioncombolist[self.focus].get() == 'Swipe':
                    text = "start x=" + str(int(self.clickstartX * self.multiple)) + ", y=" + str(int(self.clickstartY * self.multiple)) + " , " +\
                           "end x=" + str(int(self.clickendX * self.multiple)) + ", y=" + str(int(self.clickendY * self.multiple))
                    self.valuelist[self.focus].delete(0, 'end')
                    self.valuelist[self.focus].insert('end', text)

    def Dragmotion(self,event):
        self.mousePosition.set("Mouse in window [ " + str(int((event.x) * self.multiple)) + ", " + str(int((event.y) * self.multiple)) + " ]")

    def DragEnter(self, event):
        self.focusOBJImage = self.Drag_image.image

    def Dragged(self, event):
        self.Drag_image.delete("all")
        self.Drag_image.create_image(0, 0, anchor=NW, image=self.focusOBJImage)
        self.Drag_image.image = self.focusOBJImage

        self.mousePosition.set("Rectangle at [ " + str(self.clickstartX * self.multiple ) + ", " + str(self.clickstartY * self.multiple) + " To " + str((event.x) * self.multiple) + ", " + str((event.y) * self.multiple) + " ]")
        self.drawArrow(self.clickstartX, self.clickstartY, event.x, event.y)

    def drawArrow(self,fromX, fromY, toX, toY):
        angle = math.atan2(fromY - toY, fromX - toX) * 180 / math.pi
        angle1 = (angle + 30) * math.pi / 180
        angle2 = (angle - 30) * math.pi / 180
        topX = 30 * math.cos(angle1)
        topY = 30 * math.sin(angle1)
        botX = 30 * math.cos(angle2)
        botY = 30 * math.sin(angle2)

        self.Drag_image.create_line(fromX, fromY, toX, toY, fill="red", width=2)

        arrowX = toX + topX
        arrowY = toY + topY

        self.Drag_image.create_line(toX, toY, arrowX, arrowY, fill="red", width=2)

        arrowX = toX + botX
        arrowY = toY + botY

        self.Drag_image.create_line(toX, toY, arrowX, arrowY, fill="red", width=2)


if __name__ == '__main__':
    root = Tk()
    root.title("Visual Script")
    app = View(master=root)
    app.mainloop()
