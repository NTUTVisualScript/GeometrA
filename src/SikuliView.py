from tkinter import *
from tkinter import ttk
import xml.etree.cElementTree as ET
from SaveIMG import saveImg
from adb_roboot import ADBRobot
from PIL import Image, ImageTk
from TestCase import TestCase
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
        master.minsize(width=1350, height=840)

        self.formatButton()

        self.savecropImg = saveImg()

        self.ScreenShotUI()
        self.XMLTreeUI()

        self.SaveIMGButton()
        self.cropImageUI()
        self.getmouseEvent()
        self.TestCaseTable = TestCase(self.master)
        self.TestCaseTable.view()

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

    def cropImage(self, left, top, right, bottom):
        self.cropped = self.photo.crop((left, top, right, bottom))
        self.cropped.thumbnail((200, 200))
        self.tk_im = ImageTk.PhotoImage(self.cropped)
        self.crop.create_image(0, 0, anchor=NW, image=self.tk_im)

    def drawRectangle(self, left, top, right, bottom):
        self.screenshot.create_rectangle(left +3 , top + 3 , right -3 , bottom -3 , outline='red', width=2)

    def getmouseEvent(self):
        self.mousePosition = StringVar()  # displays mouse position
        self.mousePosition.set("Mouse outside window")
        self.positionLabel = Label(self.master, textvariable=self.mousePosition)
        self.positionLabel.place(x = 460, y = 270)
        self.screenshot.bind("<Button-1>", self.clickdown)  # clickdown
        self.screenshot.bind("<ButtonRelease-1>", self.clickup)  # clickup
        #self.screenshot.bind("<Motion>", self.motion)  #get mouse coordination
        # self.screenshot.bind("<Enter>", self.enteredWindow)
        # self.screenshot.bind("<Leave>", self.exitedWindow)
        self.screenshot.bind("<B1-Motion>", self.mouseDragged)  #滑鼠拖拉動作

    def clickdown(self, event):
        if filePath is None: return
        self.resetScreenShot()
        self.clickstartX = event.x
        self.clickstartY = event.y

    def clickup(self, event):
        if filePath is None: return
        self.clickendX = event.x
        self.clickendY = event.y
        self.left, self.right = sorted([self.clickendX, self.clickstartX])
        self.top, self.bottom = sorted([self.clickstartY, self.clickendY])

        self.cropImage(self.left, self.top, self.right, self.bottom)

    def motion(self,event):
        self.mousePosition.set("Mouse in window [ " + str(event.x * self.multiple) + ", " + str(event.y * self.multiple) + " ]")

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
        self.treeview["columns"] = ("one")
        self.treeview.column("one", width=150)
        self.treeview.heading("one", text="Bounds")
        self.treeview.column('#0', stretch=YES, minwidth=0, width=500)
        self.treeview.place( x = 460, y = 30)

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
                                                                   + str(elem.get('class')) + "  " + str(elem.get('text'))
                                                                   + "  ",  values=(str(elem.get('bounds'))) , open=True)
            self.tree_info(id_child, elem)

    def clear_XML_Tree(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)

    def on_tree_select(self, event):   #取得所選擇的item value  中的Bounds
        for item in self.treeview.selection():
            item_value = self.treeview.item(item, "value")

        bounds = item_value[0].split('[')
        right_bounds = bounds[1].split(']')
        left_bounds = bounds[2].split(']')

        right_top = right_bounds[0].split(',')
        left_bottom = left_bounds[0].split(',')

        self.left = int(right_top[0]) / self.multiple
        self.top = int(right_top[1]) / self.multiple
        self.right = int(left_bottom[0]) / self.multiple
        self.bottom = int(left_bottom[1]) / self.multiple
        print(str(self.right) + "\n" + str(self.top) + "\n" + str(self.left) + "\n" + str(self.bottom) + "\n" )
        self.resetScreenShot()
        self.cropImage(self.left , self.top ,
                       self.right , self.bottom)

        self.drawRectangle(self.left , self.top ,
                       self.right , self.bottom)

    def formatButton(self):
        self.dumpUI = Button(self.master, command=self.formatButtonClick, text="Dump UI",width=15)
        self.dumpUI.place(x = 0, y = 0)

    def formatButtonClick(self):
        self.getScreenShot()
        self.clear_XML_Tree()
        self.Tree_infomation()

    def SaveIMGButton(self):
        self.SaveIMG = Button(self.master, command=self.SaveIMGButtonClick, text="Save Crop Image",width=15)
        self.SaveIMG.place(x = 120, y = 0)

    def SaveIMGButtonClick(self):
        if filePath is None: return
        self.savecropImg.Save(filePath, self.getCropRange())

    def cropImageUI(self):
        self.crop = Canvas(self.master, bg='white', width=200, height=200)
        self.crop.place(x = 1130, y = 30)


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