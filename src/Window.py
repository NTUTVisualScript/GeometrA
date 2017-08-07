import os
import threading
import time
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
from TestReport import Report
from Viewtest import TestAdepter
from adb_roboot import ADBRobot
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
        self.master = master
        self.MenuBar()
        master.minsize(width=1470, height=840)
        self.focus = None
        self.focusOBJImage = None
        self.Drag_image = None
        self.tree_obj_image_list = []
        self.tree_obj_list = []
        self.dirpath = ""
        self.dirName = ""
        self.select_node = None
        self.select_image = None
        self.checkADB = checkADB_Connection()
        self.cmd = CommandManager
        self.formatButton()
        self.savecropImg = saveImg()
        self.ScreenShotUI()
        self.XMLTreeUI()
        self.MessageUI()
        #self.SaveIMGButton()
        self.RunButton()
        self.ResetButton()
        self.getmouseEvent()
        self.TestCaseFrame()

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
        self.screenshot = Canvas(self.master, bg='white', height=800, width=450)
        self.screenshot.configure(borderwidth=-1)
        self.screenshot.place( x = 0, y = 30)
        self.multiple = 1

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

        self.valueImageList[line] = self.cropped
        # print("valueImageList = " + str(line))
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
            self.add_changes(self.focus, "", self.actionList[self.focus], self.valueList[self.focus], self.valueImageList[self.focus], self.nodePathList[self.focus])

            if self.actionManuList[self.focus].get() == 'Click'or self.actionManuList[self.focus].get() == 'Assert Exist'or self.actionManuList[self.focus].get() == 'Assert Not Exist':
                self.valueList[self.focus].delete(0, 'end')
                for item in self.treeview.selection():
                    value = self.treeview.item(item, "value")
                bounds = value[1]
                left, top, right, bottom = self.bounds_split(bounds)
                self.cropImage(self.focus, left, top, right, bottom)
                self.nodePathList[self.focus] = node_path

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
                self.add_changes(line, "", self.actionList[line], self.valueList[line], self.valueImageList[line],
                                 self.nodePathList[line])
                if self.actionManuList[self.focus].get() == 'Click' or self.actionManuList[self.focus].get() == 'Assert Exist' or self.actionManuList[self.focus].get() =='Assert Not Exist':
                    self.valueList[self.focus].delete(0, 'end')
                    self.cropImage(self.focus, self.left * self.multiple, self.top * self.multiple, self.right * self.multiple, self.bottom * self.multiple)

                elif self.actionManuList[self.focus].get() == 'Drag':
                    text = "start x=" + str(int(self.clickstartX * self.multiple)) + ", y=" + str(int(self.clickstartY * self.multiple)) + " , " +\
                           "end x=" + str(int(self.clickendX * self.multiple)) + ", y=" + str(int(self.clickendY * self.multiple))
                    self.valueList[self.focus].delete(0, 'end')
                    self.valueList[self.focus].insert('end', text)

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
        #if self.actionManuList[self.focus].get() == 'Click' or self.actionManuList[self.focus].get() == 'Assert Exist':
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
            if self.actionManuList[self.focus].get() == 'Click' or self.actionManuList[self.focus].get() == 'Assert Exist' or self.actionManuList[self.focus].get() == 'Assert Not Exist':
                self.cropImage(self.focus, self.left, self.top, self.right, self.bottom)

            if self.actionManuList[self.focus].get() == 'Drag':
                text = "x=" + str( int((self.left * self.multiple + self.left * self.multiple) / 2) ) +\
                       ",y=" + str( int((self.right * self.multiple + self.left * self.bottom) / 2) )
                self.valueList[self.focus].delete(0, 'end')
                self.valueList[self.focus].insert('end', text)

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
                # self.format()
                threading.Thread(target=self.format).start()
        else:
            # self.format()
            threading.Thread(target=self.format).start()

    def format(self):
        self.clear_XML_Tree()
        if self.Drag_image != None:
            self.Drag_image.place_forget()
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
        f = Dump_UI()
        self.XMLFile = ET.ElementTree(file=f)


    def SaveIMGButton(self):
        self.SaveIMG = Button(self.master, command=self.SaveIMGButtonClick, text="Crop Image",width=15)
        self.SaveIMG.place(x = 120, y = 3)

    def SaveIMGButtonClick(self):
        # if filePath is None: return
        # self.savecropImg.Save(filePath, self.getCropRange())
        for i  in range(len(self.valueImageList)):
            if self.valueImageList[i] != None:
                #print(i)
                self.valueImageList[i].show()
                for n in range(len(self.nodePathList[i])):
                    print(self.nodePathList[i][n])

    def ShowimageButtonClick(self, line):
        self.valueImageList[line].show()

    def RunButton(self):
        self.runbutton = Button(self.master, command=self.RunButtonClick, text="Run",width=15)
        self.runbutton.place(x = 460, y = 270)

    def ResetButton(self):
        self.runbutton = Button(self.master, command=self.ResetButtonClick, text="Reset Testcase", width=15)
        self.runbutton.place(x = 580, y = 270)

    def SaveButtonClick(self):
        Save_File = SaveFile()
        self.dirpath = Save_File.SaveTestCase(self.actionManuList, self.valueList, self.valueImageList,self.nodePathList)

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
                self.actionManuList[i].set(str(actioncombo_list[i]))

                self.valueList[i].delete(0, 'end')
                self.valueList[i].insert('end', str(value_list[i]))

                self.nodePathList[i] = nodepath_list[i]
                if valueImage_list[i] != None:
                    self.valueImageList[i] = valueImage_list[i]
                    width, height = valueImage_list[i].size
                    img = valueImage_list[i].crop((0, 0, width, height))
                    img.thumbnail((100, 100))
                    image = ImageTk.PhotoImage(img)
                    self.TestcaseImage(i,image)


    def ResetButtonClick(self):
        self.TestCaseFrame()
        self.select_node = None
        self.select_image = None

    def addLineButtonClick(self,n, redoundo ):

        if redoundo ==False:
            self.add_changes( n, "add", self.actionList[n], self.valueList[n], self.valueImageList[n],
                            self.nodePathList[n])

        self.line  = self.line + 1
        self.new_line(self.line)
        i= self.line

        self.valueImageList.insert(n, None)
        self.nodePathList.insert(n, None)

        while i > n:
            getactionstr = self.actionManuList[i-1].get()
            self.actionManuList[i].set(str(getactionstr))
            self.actionManuList[i-1].set('')
            self.actionList[i] = self.actionList[i-1]
            self.actionList[i-1] = ""

            if str(type(self.valueList[i-1])) != "<class 'TestCaseEntry.TestCaseValue'>":
                self.TestcaseImage(i, self.valueList[i-1].image)
                self.TestcaseEntry(i-1)

            else:
                getvaluestr = self.valueList[i-1].get()
                self.valueList[i].delete(0, 'end')
                self.valueList[i].insert('end', getvaluestr)
                self.valueList[i - 1].delete(0, 'end')

            i=i-1


    def removeLineButtonClick(self, n, do):
        if do == False:
            self.add_changes(n, "remove", self.actionList[n], self.valueList[n], self.valueImageList[n],
                            self.nodePathList[n])

        del self.valueImageList[n]
        del self.nodePathList[n]
        i = n
        while i < self.line:
            getactionstr = self.actionManuList[i + 1].get()
            self.actionManuList[i].set(str(getactionstr))
            self.actionList[i] = self.actionList[i + 1]
            self.actionList[i + 1] = ""

            if str(type(self.valueList[i+1])) != "<class 'TestCaseEntry.TestCaseValue'>":
                self.TestcaseImage(i, self.valueList[i+1].image)
                self.TestcaseEntry(i+1)

            else:
                self.TestcaseEntry(i)
                getvaluestr = self.valueList[i+1].get()
                self.valueList[i].delete(0, 'end')
                self.valueList[i].insert('end', getvaluestr)
                self.valueList[i+1].delete(0, 'end')

            i = i + 1

        self.lineNumLIst[self.line].grid_remove()
        self.actionManuList[self.line].grid_remove()
        self.valueList[self.line].grid_remove()
        self.addLineList[self.line].grid_remove()
        self.removeLineList[self.line].grid_remove()
        self.runStepList[self.line].grid_remove()

        self.lineNumLIst.pop()
        self.actionManuList.pop()
        self.valueList.pop()
        self.addLineList.pop()
        self.removeLineList.pop()
        self.runStepList.pop()
        self.line = self.line - 1

    def runActionButtonClick(self, n):
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
            action.append(self.actionManuList[n])
            value.append(self.valueList[n])
            image.append(self.valueImageList[n])
            path_list.append(self.nodePathList[n])
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

            check_data = data.set_data(self.actionManuList, self.valueList, self.valueImageList, self.nodePathList)

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
        if len(self.testcaseUndo) != 0:
            print("undo ",self.testcaseUndo)
            testcase_line = self.testcaseUndo.pop()
            line = testcase_line[0]

            if str(type(self.valueList[line])) == "<class 'TestCaseEntry.TestCaseValue'>":
                add_redo = [line, "", self.actionManuList[line].get(), self.valueList[line].get(),
                            self.valueImageList[line], self.nodePathList[line]]
            else:
                add_redo = [line, "", self.actionManuList[line].get(), self.valueList[line].image,
                            self.valueImageList[line], self.nodePathList[line]]

            self.testcaseRedo.append(add_redo)

            print(line)
            if testcase_line[1] == "remove":
                self.addLineButtonClick(line, True)
                self.actionManuList[line].set(testcase_line[2])
                self.actionList[line] = testcase_line[2]
                print("undo ", testcase_line[2])
                if testcase_line[2] == "Click" or testcase_line[2] == "Assert Exist" or \
                     testcase_line[2] == "Assert Not Exist":
                    self.TestcaseImage(line, testcase_line[3])
                else:
                    self.TestcaseEntry(line)
                    self.valueList[line].delete(0, END)
                    self.valueList[line].insert(0, testcase_line[3])

            elif testcase_line[1] == "add":
                self.removeLineButtonClick(line, True)
            elif testcase_line[2] == "Click" or testcase_line[2] == "Assert Exist" or \
                            testcase_line[2] == "Assert Not Exist":
                self.actionManuList[line].set(testcase_line[2])
                self.TestcaseImage(line, testcase_line[3])
            else:
                self.TestcaseEntry(line)
                self.actionManuList[line].set(testcase_line[2])
                self.valueList[line].delete(0, END)
                if testcase_line[3]!= None:
                   self.valueList[line].insert(0, testcase_line[3])

            self.valueImageList[line] = testcase_line[4]
            self.nodePathList[line] = testcase_line[5]

    def redo(self):
        if len(self.testcaseRedo) != 0:
            print("redo ",self.testcaseRedo)
            testcase_line = self.testcaseRedo.pop()
            line = testcase_line[0]

            if str(type(self.valueList[line])) == "<class 'TestCaseEntry.TestCaseValue'>":
                add_undo = [line, "", self.actionManuList[line].get(), self.valueList[line].get(), self.valueImageList[line], self.nodePathList[line]]
            else:
                add_undo = [line, "", self.actionManuList[line].get(), self.valueList[line].image, self.valueImageList[line], self.nodePathList[line]]

            self.testcaseUndo.append(add_undo)

            self.actionManuList[line].set(testcase_line[2])
            if testcase_line[1] == "remove":
                self.removeLineButtonClick(line, True)
            elif testcase_line[1] == "add":
                self.addLineButtonClick(line, True)
            elif testcase_line[2] == "Click" or testcase_line[2] == "Assert Exist" or \
                            testcase_line[2] == "Assert Not Exist":
                self.TestcaseImage(line, testcase_line[3])
            else:
                self.TestcaseEntry(line)
                self.valueList[line].delete(0, END)
                if testcase_line[3] != None:
                    self.valueList[line].insert(0, testcase_line[3])

            self.valueImageList[line] = testcase_line[4]
            self.nodePathList[line] = testcase_line[5]



    def add_changes(self, line, change, action, value, image, path):
        print(str(type(value)))
        if str(type(value)) == "<class 'TestCaseEntry.TestCaseValue'>":
            testcase_line = [line, change, action, value.get(), image, path]
        else:
            testcase_line = [line, change, action, value.image, image, path]

        print(action)
        self.testcaseUndo.append(testcase_line)
        del self.testcaseRedo[:]


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

        self.lineNumLIst = []
        self.addLineList = []
        self.removeLineList = []
        self.runStepList = []
        self.actionManuList = []
        self.actionList = []
        self.valueList = []
        self.showImageList = []
        self.valueImageList = []
        self.nodePathList = []

        self.testcaseUndo = []
        self.testcaseRedo = []

        n=0
        for self.line in range(50):
            self.new_line(n)
            n=n+1

        print(self.line)

    def AuxscrollFunction(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=650, height=525)

    def TestcaseImage(self,line, image = None):
        #print("image : ",line)
        values_image = Canvas(self.listFrame, bg = "#FFFFFF",height=100, width=100)
        values_image.create_image(0, 0, anchor=NW, image=image)
        values_image.bind("<Button-1>", lambda event, i=line: self.valueFocusIn(i))
        values_image.image = image
        self.valueList[line].grid_remove()
        self.valueList[line] = values_image
        self.valueList[line].grid(row=line + 1, column=6, padx=(5, 0), pady=(5, 2.5))
        self.showImageList[line].grid(row=line + 1, column=7, padx = ( 5, 0) , pady = ( 5 , 2.5))

    def TestcaseEntry(self, line):
        value = TestCaseValue(self.listFrame, width=35)
        value.bind("<FocusIn>", lambda event, i=line: self.valueFocusIn(i))
        self.valueList[line].grid_remove()
        self.showImageList[line].grid_remove()
        self.valueList[line] = value
        self.valueList[line].grid(row=line + 1, column=6, padx=(5, 0), pady=(5, 2.5))

    def new_line(self,n):
        action_value = StringVar()

        lineStr = Label(self.listFrame, text=str(n+1)+". ", width=3)
        self.lineNumLIst.append(lineStr)
        addline = Button(self.listFrame, command=lambda :self.addLineButtonClick(n, False), text="+", width=3)
        self.addLineList.append(addline)

        removeline = Button(self.listFrame, command=lambda :self.removeLineButtonClick(n, False), text="-", width=3)
        self.removeLineList.append(removeline)

        run_single_action = Button(self.listFrame, command=lambda: self.runActionButtonClick(n), text="▶", width=3)
        self.runStepList.append(run_single_action)

        actioncombo = TestCaseAction(self.listFrame, 0, textvariable=action_value, width=10, height=22,
                                   state='readonly')
        actioncombo.bind("<<ComboboxSelected>>", lambda event, i=n: self.ActionSelect(i))
        actioncombo.bind("<MouseWheel>", lambda event, i=n: self.ActionSelect(i))
        self.actionManuList.append(actioncombo)

        value = TestCaseValue(self.listFrame,width=35)
        value.bind("<FocusIn>", lambda event, i=n: self.valueFocusIn(i))

        showimage = Button(self.listFrame, command=lambda: self.ShowimageButtonClick(n), text="show image", width=12)
        self.showImageList.append(showimage)

        self.valueList.append(value)
        self.valueImageList.append(None)
        self.nodePathList.append(None)
        self.actionList.append("")

        lineStr.grid(row = n+1 , column = 1 )
        addline.grid(row = n+1 , column = 2 )
        removeline.grid(row=n+1, column=3)
        run_single_action.grid(row=n+1, column=4)
        actioncombo.grid(row = n+1 , column = 5 , padx = ( 5 , 0 ) , pady = ( 5 , 2.5))
        value.grid(row = n+1 , column = 6 , padx = ( 5, 0) , pady = ( 5 , 2.5))

    def ActionSelect(self, n):
        self.focus = n
        #self.cmd.do(self.actionManuList[n])
        print(self.actionList[n])
        self.add_changes(n, "", self.actionList[n], self.valueList[n], self.valueImageList[n], self.nodePathList[n])
        self.actionList[n] = self.actionManuList[n].get()
        self.valueImageList[n] = None
        self.TestcaseEntry(n)
        self.Action_FocusIn()

    def valueFocusIn(self, n):
        self.focus = n
        if self.actionManuList[self.focus].get() != 'TestCase':
            self.Action_FocusIn()

    def Action_FocusIn(self):
        if self.actionManuList[self.focus].get() == 'Drag':
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

        elif self.actionManuList[self.focus].get() == 'TestCase':
            openfile = LoadFile()
            path = openfile.LoadTestCasePath()
            print(path)
            if path is not None:
                if path !="":
                    self.valueList[self.focus].delete(0, 'end')
                    self.valueList[self.focus].insert('end', path)
        elif self.actionManuList[self.focus].get() == 'Click' or self.actionManuList[self.focus].get() == 'Assert Exist' or self.actionManuList[self.focus].get() == 'Assert Not Exist':
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
                if self.actionManuList[self.focus].get() == 'Drag':
                    text = "start x=" + str(int(self.clickstartX * self.multiple)) + ", y=" + str(int(self.clickstartY * self.multiple)) + " , " +\
                           "end x=" + str(int(self.clickendX * self.multiple)) + ", y=" + str(int(self.clickendY * self.multiple))
                    self.valueList[self.focus].delete(0, 'end')
                    self.valueList[self.focus].insert('end', text)

    def Dragmotion(self,event):
        self.mousePosition.set("Mouse in window [ " + str(int((event.x) * self.multiple)) + ", " + str(int((event.y) * self.multiple)) + " ]")

    def DragEnter(self, event):
        self.focusOBJImage = self.Drag_image.image

    def Dragged(self, event):
        self.Drag_image.delete("all")
        self.Drag_image.create_image(0, 0, anchor=NW, image=self.focusOBJImage)
        self.Drag_image.image = self.focusOBJImage

        self.mousePosition.set("Rectangle at [ " + str(self.clickstartX * self.multiple ) + ", " + str(self.clickstartY * self.multiple) + " To " + str((event.x) * self.multiple) + ", " + str((event.y) * self.multiple) + " ]")
        self.Drag_image.create_line(self.clickstartX, self.clickstartY, event.x, event.y, fill="red", width=2)
        self.Drag_image.create_oval(event.x-25, event.y-25, event.x+25, event.y+25,  fill="", outline="red", width=6)

if __name__ == '__main__':
    root = Tk()
    root.title("Visual Script")
    app = View(master=root)
    app.mainloop()
