import subprocess
from tkinter import *
from tkinter import ttk
import xml.etree.cElementTree as ET
from SaveIMG import saveImg
from adb_roboot import ADBRobot
from PIL import Image, ImageTk
from Viewtest import TestAdepter
from SaveFile import SaveFile
from LoadFile import LoadFile
import time
import os

ROOT_DIR = os.path.dirname(__file__)
RESOURCES_PIC = os.path.join(ROOT_DIR, "screenshot_pic")
RESOURCES_XML = os.path.join(ROOT_DIR, "dumpXML")

filePath = None
dumpXMLfilePath = None

def IMG_PATH(name):
    return os.path.join(RESOURCES_PIC, name)

def XML_PATH(name):
    return os.path.join(RESOURCES_XML, name)

def Dump_UI():
    global dumpXMLfilePath
    robot = ADBRobot()
    dumpXMLfilePath = XML_PATH(robot.get_uiautomator_dump())
    print(dumpXMLfilePath)
    return dumpXMLfilePath

def Get_PhoneScreen():
    global filePath
    robot = ADBRobot()
    filePath = IMG_PATH(robot.screenshot())
    print(filePath)
    return filePath

class View(Frame):
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
        self.formatButton()
        self.savecropImg = saveImg()
        self.ScreenShotUI()
        self.XMLTreeUI()
        self.MessageUI()
        self.SaveIMGButton()
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

    def MessageUI(self):
        self.messagetitle = Label(self.master, text="Message Log", font=("Helvetica",16))
        self.messagetitle.place(x=1150, y=30)
        self.message = Text(self.master, bg='white', height=32, width=25, font=("Helvetica",16))
        #self.message.config(state=DISABLED)
        self.message.place(x=1150, y=60)

    def ScreenShotUI(self):
        self.screenshot = Canvas(self.master, bg='white', height=800, width=450)
        self.screenshot.configure(borderwidth=-1)
        self.screenshot.place( x = 0, y = 30)
        self.screenshot.place_info().get('x')
        self.multiple = 1

    def getScreenShot(self):
        self.screenshot.delete("all")
        self.photo = Image.open(Get_PhoneScreen())
        self.photo_width, self.photo_height = self.photo.size
        print(str(self.photo_width) + " , " + str(self.photo_height))
        self.photo.thumbnail((450, 800))
        self.width, self.height = self.photo.size
        self.multiple = self.photo_width / self.width
        print(str(self.multiple))
        self.screenshot_photo = ImageTk.PhotoImage(self.photo)
        self.screenshot.create_image(0, 0, anchor=NW)
        self.screenshot.image = self.screenshot_photo

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

        if self.focus != None:
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
                if self.actioncombolist[self.focus].get() == 'Click' or self.actioncombolist[self.focus].get() == 'Assert Exist' or self.actioncombolist[self.focus].get() =='Assert Not Exist':
                    self.valuelist[self.focus].delete(0, 'end')
                    self.cropImage(self.focus, self.left * self.multiple, self.top * self.multiple, self.right * self.multiple, self.bottom * self.multiple)

                elif self.actioncombolist[self.focus].get() == 'Drag':
                    text = "start x=" + str(int(self.clickstartX * self.multiple)) + ", y=" + str(int(self.clickstartY * self.multiple)) + " , " +\
                           "end x=" + str(int(self.clickendX * self.multiple)) + ", y=" + str(int(self.clickendY * self.multiple))
                    self.valuelist[self.focus].delete(0, 'end')
                    self.valuelist[self.focus].insert('end', text)

    def motion(self,event, line):
        x = int(self.tree_obj_image_list[line][1].place_info().get('x'))
        y = int(self.tree_obj_image_list[line][1].place_info().get('y'))
        self.mousePosition.set("Mouse in window [ " + str(int((x + event.x) * self.multiple)) + ", " + str(int((y + event.y) * self.multiple)) + " ]")

    def mouseEnter(self, event, line, w, h):
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
        self.treeview.heading("two", text="Bounds")

        self.Yvertscroll.config(command=self.treeview.yview)
        self.Xvertscroll.config(command=self.treeview.xview)

        self.treeview.bind("<ButtonRelease-1>", self.on_tree_select)

    def Tree_infomation(self):
        self.XMLFile = ET.ElementTree(file=Dump_UI())
        if self.tree_obj_image_list != None:
            del self.tree_obj_image_list[:]
            del self.tree_obj_list[:]
        self.rankMax = 0
        self.tree_info("", 0, self.XMLFile)
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
        print(obj_image_info)
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

    def on_tree_select(self, event):   #取得所選擇的item value  中的Bounds
        for item in self.treeview.selection():
            item_value = self.treeview.item(item, "value")

        self.left, self.top, self.right, self.bottom = self.bounds_split(item_value[1])

        #print(str(self.left) + "\n" + str(self.top) + "\n" + str(self.right) + "\n" + str(self.bottom) + "\n" )
        self.resetScreenShot()
        #print(self.focus)
        if self.focus != None:
            if self.actioncombolist[self.focus].get() == 'Click' or self.actioncombolist[self.focus].get() == 'Assert Exist' or self.actioncombolist[self.focus].get() == 'Assert Not Exist':
                self.cropImage(self.focus, self.left, self.top, self.right, self.bottom)

            if self.actioncombolist[self.focus].get() == 'Drag':
                text = "x=" + str( int((self.left * self.multiple + self.left * self.multiple) / 2) ) +\
                       ",y=" + str( int((self.right * self.multiple + self.left * self.bottom) / 2) )
                self.valuelist[self.focus].delete(0, 'end')
                self.valuelist[self.focus].insert('end', text)

    def formatButton(self):
        self.dumpUI = Button(self.master, command=self.formatButtonClick, text="Dump UI",width=15)
        self.dumpUI.place(x = 0, y = 3)

    def formatButtonClick(self, getdevices =None):
        self.focus = None
        if getdevices ==None:
            self.message.delete(1.0, END)
            if self.checkADB_Connection() == "Connect":
                self.clear_XML_Tree()
                self.getScreenShot()
                self.Tree_infomation()
        else:
            self.clear_XML_Tree()
            self.getScreenShot()
            self.Tree_infomation()


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
        Save_File.SaveTestCase(self.actioncombolist, self.valuelist, self.valueImagelist,self.node_path_list)

    def LoadButtonClick(self):
        Load_File = LoadFile()
        dirpath = Load_File.LoadTestCasePath()
        if  dirpath != None:
            print("dirpath : ", dirpath)
            self.ResetButtonClick()
            Load_File.Decoder_Json(dirpath)
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

    def AddLineButtonClick(self,n):
        self.line  = self.line + 1
        self.new_line(self.line)
        i= self.line

        self.valueImagelist.insert(n, None)
        self.node_path_list.insert(n, None)

        while i > n:
            getactionstr = self.actioncombolist[i-1].get()
            self.actioncombolist[i].set(str(getactionstr))
            self.actioncombolist[i-1].set('')

            if getactionstr == "Click" or getactionstr == "Assert Exist" or getactionstr == "Assert Not Exist":
                self.TestcaseImage(i, self.valuelist[i-1].image)
                self.TestcaseEntry(i-1)

            else:
                getvaluestr = self.valuelist[i-1].get()
                self.valuelist[i].delete(0, 'end')
                self.valuelist[i].insert('end', getvaluestr)
                self.valuelist[i - 1].delete(0, 'end')

            i=i-1

    def RemoveLineButtonClick(self,n):
        del self.valueImagelist[n]
        del self.node_path_list[n]
        i = n
        while i < self.line:
            getactionstr = self.actioncombolist[i + 1].get()
            self.actioncombolist[i].set(str(getactionstr))

            if getactionstr == "Click" or getactionstr == "Assert Exist" or getactionstr =="Assert Not Exist":
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
        run = TestAdepter()
        self.message.delete(1.0, END)
        if self.checkADB_Connection() == "Connect":
            status = "Success"
            status = run.Single_Test(self.actioncombolist[n], self.valuelist[n], self.valueImagelist[n], self.node_path_list[n])
            if status == "Error":
                statusstr = "Action " + str(n + 1) + " Status Error\n"
                self.message.insert('end', statusstr)
            else:
                statusstr = "Action " + str(n + 1) + " Status Success\n"
                self.message.insert('end', statusstr)

            self.formatButtonClick("no")

    def TestCaseData(self, actioncombolist, valuelist, valueImagelist, node_path_list):
        action = []
        value = []
        image = []
        path_list = []

        for i in range(len(actioncombolist)):
            action.append(actioncombolist[i].get())
            if valueImagelist[i] != None:
                value.append(None)
            else:
                value.append(valuelist[i].get())
            if i < len(valueImagelist):
                image.append(valueImagelist[i])
                path_list.append(node_path_list[i])
        return action, value, image, path_list


    def RunButtonClick(self):
        run = TestAdepter()
        self.message.delete(1.0, END)
        if self.checkADB_Connection() =="Connect":
            self.start = None
            self.end = None
            self.forloop = None
            for i in range(len(self.actioncombolist)):
                if self.actioncombolist[i].get() != "":
                    if self.actioncombolist[i].get() == "Loop":
                        self.start = i + 1
                        if self.valuelist[i].get() == "":
                            statusstr = "Action " + str(i + 1) + " Status Error\nForLoop no Input times\nTest Case Interrupted!\n"
                            self.message.insert('end', statusstr)
                            break
                        else:
                            self.forloop = int(self.valuelist[i].get()) - 1
                    elif self.actioncombolist[i].get() == "Stop":
                        self.end = i
                        self.ForLoop(self.actioncombolist, self.valuelist, self.valueImagelist, self.node_path_list)
                    elif self.actioncombolist[i].get() == "Sleep(s)":
                        time.sleep(int(self.valuelist[i].get()))
                        print(self.valuelist[i].get())
                    else:
                        status = run.Single_Test(self.actioncombolist[i], self.valuelist[i], self.valueImagelist[i],
                                    self.node_path_list[i])
                        if status == "Error":
                            statusstr = "Action "+ str(i+1) + " Status Error\nTest Case Interrupted!\n"
                            self.message.insert('end', statusstr)
                            break
                        else:
                            statusstr = "Action "+ str(i+1) + " Status Success\n"
                            self.message.insert('end', statusstr)
                    if i == len(self.actioncombolist) - 1 and self.end == None and self.start != None:
                        statusstr = "Action ForLoop Status Error\nForLoop no set stop\nTest Case Interrupted!\n"
                        self.message.insert('end', statusstr)
                        break

            finish = "The Test Case Finish!"
            self.message.insert('end', finish)
            self.formatButtonClick("no")

    def ForLoop(self, actioncombo_list, value_list, valueImage_list, nodepath_list):
        if self.CheckLoop():
            run = TestAdepter()
            for i in range(self.forloop):
                index = self.start
                while index < self.end:
                    if actioncombo_list[index].get() != "":
                        status = run.Single_Test(actioncombo_list[index], value_list[index], valueImage_list[index],
                                                 nodepath_list[index])
                        index = index + 1
                        if status == "Error":
                            break
        else:
            status =  "Error"

        self.forloop = None
        self.start = None
        self.end = None
        return status

    def CheckLoop(self):
        if self.forloop!=None and self.start!=None and self.end != None:
            return True
        else:
            return False


    def checkADB_Connection(self):
        try:
            deviceInfo = subprocess.getoutput('adb devices')
            self.deviceNames = deviceInfo.splitlines()
            print(self.deviceNames)
            finddevices = []
            for i in range(len(self.deviceNames)):
                if self.deviceNames[i].find("emulator") >= 0:
                    subprocess.check_call('adb kill-server')
                    self.checkADB_Connection()

                if self.deviceNames[i].find("device") >= 0:
                    finddevices.append(self.deviceNames[i])

            finddevices.pop(0)

            if len(finddevices) == 0:
                self.message.insert(END, "No Devices connect...\n")
                return "No Connect"
            else:
                self.message.insert(END, "Get devices :\n")
                for i in range(len(finddevices)):
                    self.message.insert(END, finddevices[i] + "\n\n\n")
                return "Connect"

        except subprocess.CalledProcessError as e:
            self.message.insert(END, e.returncode)


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
        self.valuelist = []
        self.showimagelist = []
        self.valueImagelist = []
        self.node_path_list = []

        n=0
        for self.line in range(50):
            self.new_line(n)
            n=n+1

    def AuxscrollFunction(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=650, height=525)

    def TestcaseImage(self,line, image):
        #print("image : ",line)
        values_image = Canvas(self.listFrame, height=100, width=100)
        values_image.create_image(0, 0, anchor=NW, image=image)
        values_image.bind("<Button-1>", lambda event, i=line: self.valueFocusIn(event, i))
        values_image.image = image
        self.valuelist[line].grid_remove()
        self.valuelist[line] = values_image
        self.valuelist[line].grid(row=line + 1, column=6, padx=(5, 0), pady=(5, 2.5))
        self.showimagelist[line].grid(row=line + 1, column=7, padx = ( 5, 0) , pady = ( 5 , 2.5))

    def TestcaseEntry(self, line):
        value = Entry(self.listFrame, width=35)
        value['font'] = ('Times', 13, 'bold italic')
        value.bind("<FocusIn>", lambda event, i=line: self.valueFocusIn(event, i))
        self.valuelist[line].grid_remove()
        self.showimagelist[line].grid_remove()
        self.valuelist[line] = value
        self.valuelist[line].grid(row=line + 1, column=6, padx=(5, 0), pady=(5, 2.5))

    def new_line(self,n):
        action_value = StringVar()

        lineStr = Label(self.listFrame, text=str(n+1)+". ", width=3)
        self.lineStrlist.append(lineStr)
        addline = Button(self.listFrame, command=lambda:self.AddLineButtonClick(n), text="+", width=3)
        self.addlinelist.append(addline)

        removeline = Button(self.listFrame, command=lambda:self.RemoveLineButtonClick(n), text="-", width=3)
        self.removelinelist.append(removeline)

        run_single_action = Button(self.listFrame, command=lambda: self.Run_single_actionButtonClick(n), text="▶", width=3)
        self.run_single_actionlist.append(run_single_action)

        actioncombo = ttk.Combobox(self.listFrame, textvariable=action_value, width=10, height=22,
                                   state='readonly')
        actioncombo['values'] = ('', 'Click', 'Drag', 'Input', 'TestCase', 'Loop', 'Stop', 'Sleep(s)', 'Android Keycode', 'Assert Exist', 'Assert Not Exist')
        actioncombo['font'] = ('Times', 11, 'bold italic')
        actioncombo.bind("<<ComboboxSelected>>", lambda event, i=n: self.ActionSelect(event, i))
        actioncombo.bind("<MouseWheel>", lambda event, i=n: self.ActionSelect(event, i))
        actioncombo.current(0)
        self.actioncombolist.append(actioncombo)

        value = Entry(self.listFrame,width=35)
        value['font'] = ('Times', 13, 'bold italic')
        value.bind("<FocusIn>", lambda event, i=n: self.valueFocusIn(event, i))

        showimage = Button(self.listFrame, command=lambda: self.ShowimageButtonClick(n), text="show image", width=12)
        self.showimagelist.append(showimage)

        self.valuelist.append(value)
        self.valueImagelist.append(None)
        self.node_path_list.append(None)

        lineStr.grid(row = n+1 , column = 1 )
        addline.grid(row = n+1 , column = 2 )
        removeline.grid(row=n+1, column=3)
        run_single_action.grid(row=n+1, column=4)
        actioncombo.grid(row = n+1 , column = 5 , padx = ( 5 , 0 ) , pady = ( 5 , 2.5))
        value.grid(row = n+1 , column = 6 , padx = ( 5, 0) , pady = ( 5 , 2.5))

    def ActionSelect(self,event, n):
        self.focus = n
        self.valueImagelist[n] = None
        self.TestcaseEntry(n)
        self.Action_FocusIn()

    def valueFocusIn(self,event, n):
        self.focus = n

    def Action_FocusIn(self):
        if self.actioncombolist[self.focus].get() == 'Drag':
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
            if path is not None:
                if path !="":
                    self.valuelist[self.focus].delete(0, 'end')
                    self.valuelist[self.focus].insert('end', path)
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
                if self.actioncombolist[self.focus].get() == 'Drag':
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
        self.Drag_image.create_line(self.clickstartX, self.clickstartY, event.x, event.y, fill="red", width=2)

if __name__ == '__main__':
    root = Tk()
    root.title("Visual Script")
    app = View(master=root)
    app.mainloop()