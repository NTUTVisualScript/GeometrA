from tkinter import *
from tkinter import ttk
import xml.etree.cElementTree as ET
from SaveIMG import saveImg
from adb_roboot import ADBRobot
from PIL import Image, ImageTk
from Viewtest import TestAdepter
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
        master.minsize(width=1150, height=840)
        self.formatButton()
        self.savecropImg = saveImg()
        self.ScreenShotUI()
        self.XMLTreeUI()
        self.SaveIMGButton()
        self.RunButton()
        self.SaveButton()
        self.ResetButton()
        self.getmouseEvent()
        self.TestCaseFrame()

    def ScreenShotUI(self):
        self.screenshot = Canvas(self.master, bg='white', height=800, width=450)
        self.screenshot.place( x = 0, y = 30)
        self.multiple = 1

    def getScreenShot(self):
        self.photo = Image.open(Get_PhoneScreen())
        self.photo_width, self.photo_height = self.photo.size
        print(str(self.photo_width) + " , " + str(self.photo_height))
        self.photo.thumbnail((450, 800))
        self.width, self.height = self.photo.size
        self.multiple = self.photo_width / self.width
        print(str(self.multiple))
        self.screenshot_photo = ImageTk.PhotoImage(self.photo)
        self.screenshot.create_image(0, 0, anchor=NW, image=self.screenshot_photo)

    def getImgPath(self):
        return filePath

    def getCropRange(self):
        return self.left, self.top, self.right, self.bottom, self.multiple

    def resetScreenShot(self):
        self.screenshot.delete("all")
        self.screenshot.create_image(0, 0, anchor=NW, image=self.screenshot_photo)

    def cropImage(self,line, left, top, right, bottom):
        photo = Image.open(filePath)
        self.cropped = photo.crop((left * self.multiple, top * self.multiple, right * self.multiple, bottom * self.multiple))

        self.valueImagelist[line] = self.cropped
        print("valueImagelist size = " + str(len(self.valueImagelist)))

        img = self.photo.crop((left, top, right, bottom))
        img.thumbnail((100, 100))
        self.image = ImageTk.PhotoImage(img)
        self.TestcaseImage(line, self.image)


    def drawRectangle(self, left, top, right, bottom):
        self.screenshot.create_rectangle(left +3 , top + 3 , right -3 , bottom -3 , outline='red', width=2)

    def getmouseEvent(self):
        self.mousePosition = StringVar()  # displays mouse position
        self.mousePosition.set("Mouse outside window")
        self.positionLabel = Label(self.master, textvariable=self.mousePosition)
        self.positionLabel.place(x = 820, y = 270)
        self.screenshot.bind("<Button-1>", self.clickdown)  # clickdown
        self.screenshot.bind("<ButtonRelease-1>", self.clickup)  # clickup
        self.screenshot.bind("<Motion>", self.motion)  #get mouse coordination
        self.screenshot.bind("<B1-Motion>", self.mouseDragged)  #滑鼠拖拉動作

    def clickdown(self, event):
        if filePath is None: return
        self.resetScreenShot()
        self.clickstartX = event.x
        self.clickstartY = event.y
        if self.focus != None:
            if self.typecombolist[self.focus].get() == 'coordinate':
                text = "x=" + str(int(event.x * self.multiple)) + ",y=" + str(int(event.y * self.multiple))
                self.valuelist[self.focus].delete(0, 'end')
                self.valuelist[self.focus].insert('end',text)

    def clickup(self, event):
        if filePath is None: return
        self.clickendX = event.x
        self.clickendY = event.y
        self.left, self.right = sorted([self.clickendX, self.clickstartX])
        self.top, self.bottom = sorted([self.clickstartY, self.clickendY])

        if self.left != self.right and self.top != self.bottom:
            if self.focus != None:
                if self.typecombolist[self.focus].get() == 'image' or self.typecombolist[self.focus].get() == 'find' \
                        or self.typecombolist[self.focus].get() == 'to':
                    self.valuelist[self.focus].delete(0, 'end')
                    self.cropImage(self.focus, self.left, self.top, self.right, self.bottom)

                elif self.typecombolist[self.focus].get() == 'coordinate':
                    text = "start x=" + str(int(self.clickstartX * self.multiple)) + ", y=" + str(int(self.clickstartY * self.multiple)) + " , " +\
                           "end x=" + str(int(event.x * self.multiple)) + ", y=" + str(int(event.y * self.multiple))
                    self.valuelist[self.focus].delete(0, 'end')
                    self.valuelist[self.focus].insert('end', text)

    def motion(self,event):
        self.mousePosition.set("Mouse in window [ " + str(int(event.x * self.multiple)) + ", " + str(int(event.y * self.multiple)) + " ]")

    def mouseDragged(self, event):
        if filePath is None: return
        self.screenshot.create_image(0, 0, anchor=NW, image=self.screenshot_photo)
        if event.x < 0 :
            event.x = 0
        if event.y < 0 :
            event.y = 0
        if event.x > self.screenshot_photo.width():
            event.x = self.screenshot_photo.width()
        if event.y > self.screenshot_photo.height():
            event.y = self.screenshot_photo.height()

        self.drawRectangle(self.clickstartX, self.clickstartY, event.x, event.y )
        self.mousePosition.set("Rectangle at [ " + str(self.clickstartX * self.multiple ) + ", " + str(self.clickstartY * self.multiple) + " To " + str(event.x * self.multiple) + ", " + str(event.y * self.multiple) + " ]")

    def XMLTreeUI(self):
        self.Yvertscroll = Scrollbar(self.master, orient=VERTICAL)
        #self.Yvertscroll.pack( side = RIGHT, fill=Y )

        self.Xvertscroll = Scrollbar(self.master, orient=HORIZONTAL)
        #self.Xvertscroll.grid(column=25 + 1, row=18, rowspan=1, columnspan=20, sticky='WE')

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

        self.treeview.bind("<<TreeviewSelect>>", self.on_tree_select)

    def Tree_infomation(self):
        self.XMLFile = ET.ElementTree(file=Dump_UI())
        self.tree_info("", self.XMLFile)

    def tree_info(self,id , treeinfo):
        for elem in treeinfo.findall('node'):
            if elem is None: return
            id_child = self.treeview.insert(id, "end", elem , text="(" + str(elem.get('index')) + ") "
                                                                   + str(elem.get('class')) + "  "
                                                                   ,  values=( str(elem.get('text')),str(elem.get('bounds'))) , open=True)
            self.tree_info(id_child, elem)

    def clear_XML_Tree(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)

    def on_tree_select(self, event):   #取得所選擇的item value  中的Bounds

        for item in self.treeview.selection():
            item_value = self.treeview.item(item, "value")

        print(item_value)
        bounds = item_value[1].split('[')
        right_bounds = bounds[1].split(']')
        left_bounds = bounds[2].split(']')

        right_top = right_bounds[0].split(',')
        left_bottom = left_bounds[0].split(',')

        self.left = int(right_top[0]) / self.multiple
        self.top = int(right_top[1]) / self.multiple
        self.right = int(left_bottom[0]) / self.multiple
        self.bottom = int(left_bottom[1]) / self.multiple
        print(str(self.left) + "\n" + str(self.top) + "\n" + str(self.right) + "\n" + str(self.bottom) + "\n" )
        self.resetScreenShot()

        if self.focus != None:
            if self.typecombolist[self.focus].get() == 'image' or self.typecombolist[self.focus].get() == 'find'\
                    or self.typecombolist[self.focus].get() == 'to':
                self.cropImage(self.focus, self.left, self.top, self.right, self.bottom)

            if self.typecombolist[self.focus].get() == 'text':
                self.valuelist[self.focus].delete(0, 'end')
                self.valuelist[self.focus].insert('end', item_value[0])

            if self.typecombolist[self.focus].get() == 'coordinate':
                text = "x=" + str( int((int(right_top[0]) + int(left_bottom[0])) / 2) ) +\
                       ",y=" + str( int((int(right_top[1]) + int(left_bottom[1])) / 2) )
                self.valuelist[self.focus].delete(0, 'end')
                self.valuelist[self.focus].insert('end', text)

        self.drawRectangle(self.left , self.top ,
                       self.right , self.bottom)

    def formatButton(self):
        self.dumpUI = Button(self.master, command=self.formatButtonClick, text="Dump UI",width=15)
        self.dumpUI.place(x = 0, y = 3)

    def formatButtonClick(self):
        os.popen("adb kill-server")
        time.sleep(1)
        os.popen("adb devices")
        time.sleep(5)
        self.getScreenShot()
        self.clear_XML_Tree()
        self.Tree_infomation()

    def SaveIMGButton(self):
        self.SaveIMG = Button(self.master, command=self.SaveIMGButtonClick, text="Crop Image",width=15)
        self.SaveIMG.place(x = 120, y = 3)

    def SaveIMGButtonClick(self):
        # if filePath is None: return
        # self.savecropImg.Save(filePath, self.getCropRange())
        for i  in range(len(self.valueImagelist)):
            if self.valueImagelist[i] != None:
                print(i)
                self.valueImagelist[i].show()

    def RunButton(self):
        self.runbutton = Button(self.master, command=self.RunButtonClick, text="Run",width=15)
        self.runbutton.place(x = 460, y = 270)

    def SaveButton(self):
        self.runbutton = Button(self.master, text="Save Testcase",width=15)
        self.runbutton.place(x = 580, y = 270)

    def ResetButton(self):
        self.runbutton = Button(self.master, command=self.ResetButtonClick, text="Reset Testcase", width=15)
        self.runbutton.place(x=700, y=270)

    def ResetButtonClick(self):
        self.TestCaseFrame()

    def AddLineButtonClick(self,n):
        self.line  = self.line + 1
        self.new_line(self.line)
        i= self.line

        self.valueImagelist.insert(n, None)

        while i > n:
            getactionstr = self.actioncombolist[i-1].get()
            self.actioncombolist[i].set(str(getactionstr))
            self.actioncombolist[i-1].set('')

            gettypestr = self.typecombolist[i-1].get()
            self.typecombolist[i].set(str(gettypestr))
            self.typecombolist[i-1].set("")

            if gettypestr == "image" or gettypestr == "find" or gettypestr == "to":
                self.TestcaseImage(i, self.valuelist[i-1].image)
                self.TestcaseEntry(i-1)

            else:
                getvaluestr = self.valuelist[i-1].get()
                self.valuelist[i].delete(0, 'end')
                self.valuelist[i].insert('end', getvaluestr)
                self.valuelist[i - 1].delete(0, 'end')

            i=i-1

        #self.valueImagelist[n + 1].close()


    def RemoveLineButtonClick(self,n):
        del self.valueImagelist[n]
        i = n
        while i < self.line:
            getactionstr = self.actioncombolist[i + 1].get()
            self.actioncombolist[i].set(str(getactionstr))

            gettypestr = self.typecombolist[i+1].get()
            self.typecombolist[i].set(str(gettypestr))

            if gettypestr == "image" or gettypestr == "find" or gettypestr == "to":
                self.TestcaseImage(i, self.valuelist[i+1].image)
                self.TestcaseEntry(i+1)

            else:
                self.TestcaseEntry(i)
                getvaluestr = self.valuelist[i+1].get()
                self.valuelist[i].delete(0, 'end')
                self.valuelist[i].insert('end', getvaluestr)
                self.valuelist[i+1].delete(0, 'end')

            i = i + 1

        self.actioncombolist[self.line].grid_remove()
        self.typecombolist[self.line].grid_remove()
        self.valuelist[self.line].grid_remove()
        self.addlinelist[self.line].grid_remove()
        self.removelinelist[self.line].grid_remove()

        self.actioncombolist.pop()
        self.typecombolist.pop()
        self.valuelist.pop()
        self.addlinelist.pop()
        self.removelinelist.pop()
        self.line = self.line - 1


    def RunButtonClick(self):
        run = TestAdepter()
        run.Test(self.actioncombolist, self.typecombolist, self.valuelist, self.valueImagelist)

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

        self.addlinelist = []
        self.removelinelist = []
        self.actioncombolist = []
        self.typecombolist = []
        self.valuelist = []
        self.valueImagelist = []

        n=0
        for self.line in range(50):
            self.new_line(n)
            n=n+1

    def AuxscrollFunction(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=650, height=525)

    def TestcaseImage(self,line, image):
        print("image : ",line)
        values_image = Canvas(self.listFrame, height=100, width=100)
        values_image.create_image(0, 0, anchor=NW, image=image)
        values_image.image = image
        self.valuelist[line].grid_remove()
        self.valuelist[line] = values_image
        self.valuelist[line].grid(row=line + 1, column=5, padx=(5, 0), pady=(5, 2.5))

    def TestcaseEntry(self, line):
        value = Entry(self.listFrame, width=37)
        value['font'] = ('Times', 13, 'bold italic')
        value.bind("<FocusIn>", lambda event, i=line: self.valueFocusIn(event, i))
        self.valuelist[line].grid_remove()
        self.valuelist[line] = value
        self.valuelist[line].grid(row=line + 1, column=5, padx=(5, 0), pady=(5, 2.5))

    def new_line(self,n):
        action_value = StringVar()
        type_value = StringVar()

        addline = Button(self.listFrame, command=lambda:self.AddLineButtonClick(n), text="+", width=3)
        self.addlinelist.append(addline)

        removeline = Button(self.listFrame, command=lambda:self.RemoveLineButtonClick(n), text="-", width=3)
        self.removelinelist.append(removeline)

        actioncombo = ttk.Combobox(self.listFrame, textvariable=action_value, width=10, height=22,
                                   state='readonly')
        actioncombo['values'] = ('', 'Click', 'Drag', 'Input', 'Exists')
        actioncombo['font'] = ('Times', 11, 'bold italic')
        actioncombo.bind("<<ComboboxSelected>>", lambda event, i=n: self.ActionSelect(event, i))
        actioncombo.current(0)
        self.actioncombolist.append(actioncombo)

        typecombo = ttk.Combobox(self.listFrame, textvariable=type_value, width=10, height=22,
                                 state='readonly')
        typecombo['font'] = ('Times', 11, 'bold italic')
        typecombo.bind("<<ComboboxSelected>>", lambda event, i=n: self.TypeSelect(event, i))
        self.typecombolist.append(typecombo)

        value = Entry(self.listFrame,width=37)
        value['font'] = ('Times', 13, 'bold italic')
        value.bind("<FocusIn>", lambda event, i=n: self.valueFocusIn(event, i))

        self.valuelist.append(value)
        self.valueImagelist.append(None)

        addline.grid(row = n+1 , column = 1 )
        removeline.grid(row=n+1, column=2)
        actioncombo.grid(row = n+1 , column = 3 , padx = ( 5 , 0 ) , pady = ( 5 , 2.5))
        typecombo.grid(row = n+1 , column = 4 , padx = ( 5 , 0 ) , pady = ( 5 , 2.5))
        value.grid(row = n+1 , column = 5 , padx = ( 5, 0) , pady = ( 5 , 2.5))

    def ActionSelect(self,event, n):
        item = self.actioncombolist[n]
        self.typecombolist[n].grid_remove()
        if item.get() == "Click":
            typevalue = self.typecombolist[n]
            typevalue['values'] = ('', 'text', 'image', 'find', 'coordinate')
            typevalue.current(0)
            self.typecombolist[n] = typevalue

        elif item.get() == "Drag":
            typevalue = self.typecombolist[n]
            typevalue['values'] = ('', 'find', 'to', 'coordinate')
            typevalue.current(0)
            self.typecombolist[n] = typevalue

        elif item.get() == "Assert":
            typevalue = self.typecombolist[n]
            typevalue['values'] = ('', 'image', 'text', 'no image', 'no text')
            typevalue.current(0)
            self.typecombolist[n] = typevalue

        else:
            typevalue = self.typecombolist[n]
            typevalue['values'] = ('')
            typevalue.set('')
            self.typecombolist[n] = typevalue
            self.valuelist[n].grid_remove()
            self.TestcaseEntry(n)

        self.typecombolist[n].grid(row=n + 1, column=4, padx=(5, 0), pady=(5, 2.5))


    def TypeSelect(self,event, n):
        self.valuelist[n].grid_remove()
        value = Entry(self.listFrame, width=37)
        value['font'] = ('Times', 13, 'bold italic')
        value.bind("<FocusIn>", lambda event, i=n: self.valueFocusIn(event, i))
        self.valuelist[n] = value
        self.valuelist[n].grid(row=n + 1, column=5, padx=(5, 0), pady=(5, 2.5))

    def valueFocusIn(self,event, n):
        self.focus = n
        print(n)

if __name__ == '__main__':
    root = Tk()
    root.title("Sikuli Viewer")
    app = View(master=root)
    app.mainloop()

# from tkinter import *
# from DumpXML import *
# from SaveIMG import saveImg
# from DumpScreenShot import *
# from PIL import Image, ImageTk
# import os
#
# ROOT_DIR = os.path.dirname(__file__)
# RESOURCES_DIR = os.path.join(ROOT_DIR, "resources/taipeibus")
#
# def IMG_PATH(name):
#     return os.path.join(RESOURCES_DIR, name)
#
# class View(Frame):
#     def __init__(self, master=None):
#         Frame.__init__(self, master)
#         master.minsize(width=1350, height=840)
#         self.grid()
#         self.formatButton()
#
#         self.treeUI = dump(self.master)
#         self.screenshotUI = dumpscreenshot(self.master)
#         self.savecropImg = saveImg()
#
#         self.screenshotUI.ScreenShotUI()
#         self.treeUI.XMLTreeUI()
#
#         self.SaveIMGButton()
#         self.cropImageUI()
#         self.screenshotUI.getmouseEvent()
#
#     def formatButton(self):
#         self.dumpUI = Button(self.master, command=self.formatButtonClick, text="Dump UI")
#         self.dumpUI.grid(row=0, column=0, rowspan=2, columnspan = 5)
#
#     def formatButtonClick(self):
#         self.screenshotUI.getScreenShot()
#         self.treeUI.clear_XML_Tree()
#         self.treeUI.Tree_infomation()
#
#     def SaveIMGButton(self):
#         self.SaveIMG = Button(self.master, command=self.SaveIMGButtonClick, text="Save Crop Image")
#         self.SaveIMG.grid(row=0, column=6, rowspan=3, columnspan=8)
#
#     def SaveIMGButtonClick(self):
#         ImgPath = self.screenshotUI.getImgPath()
#         if ImgPath is None: return
#         self.savecropImg.Save(ImgPath, self.screenshotUI.getCropRange())
#
#     def cropImageUI(self):
#         self.crop = Canvas(self.master, bg='white', width=200, height=200)
#         self.crop.grid(column=25 + 1, row=24)
#
#
# if __name__ == '__main__':
#     root = Tk()
#     root.title("Sikuli Viewer")
#     app = View(master=root)
#     app.mainloop()