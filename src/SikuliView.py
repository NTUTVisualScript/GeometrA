from tkinter import *
from adb_roboot import ADBRobot
from PIL import Image, ImageTk
import xml.etree.cElementTree as ET
import os

ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources/taipeibus")

filePath = None
dumpfilePath = None

def IMG_PATH(name):
    return os.path.join(RESOURCES_DIR, name)

def Get_PhoneScreen():
    global filePath
    robot = ADBRobot()
    filePath = IMG_PATH(robot.screenshot())
    print(filePath)
    return filePath

def Dump_UI():
    global dumpfilePath
    robot = ADBRobot()
    dumpfilePath = IMG_PATH(robot.get_uiautomator_dump())
    print(dumpfilePath)
    return dumpfilePath


class View(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.getScreenShot()
        self.getXMLTree()
        self.cropImage()
        self.getmouseEvent()

    def getScreenShot(self):
        self.photo = Image.open(Get_PhoneScreen())
        self.photo_width, self.photo_height = self.photo.size
        print(str(self.photo_width) +" , " + str(self.photo_height))
        self.photo.thumbnail((500, 800))
        self.width, self.height = self.photo.size
        self.resize = self.photo_width / self.width
        print(str(self.resize))
        self.screenshot = Canvas(self.master, bg='white', height=self.height-1, width=self.width-1)
        self.screenshot.grid(row=0, column=0, rowspan=self.height, columnspan = self.width)
        self.screenshot_photo = ImageTk.PhotoImage(self.photo)
        self.screenshot.create_image(0, 0, anchor=NW, image=self.screenshot_photo)

    def getXMLTree(self):
        self.XMLTree = Listbox(self.master, height=15, width=80)
        self.XMLTree.grid(column=self.width + 1, row=0, rowspan=15, columnspan=80)

        self.vertscroll = Scrollbar(self.master, orient=VERTICAL)
        self.vertscroll.config(command=self.XMLTree.yview)
        self.vertscroll.grid(column=self.width + 82, row=0, rowspan=15, columnspan=1, sticky='NS')

        self.Xvertscroll = Scrollbar(self.master, orient=HORIZONTAL)
        self.Xvertscroll.config(command=self.XMLTree.xview)
        self.Xvertscroll.grid(column=self.width + 1, row=16 , rowspan=1, columnspan=82, sticky='WE')

        self.XMLTree.config(yscrollcommand=self.vertscroll.set)
        self.XMLTree.config(xscrollcommand=self.Xvertscroll.set)

        self.tree = ET.ElementTree(file = Dump_UI())
        self.tree_bounds(self.tree, 0)

    def tree_bounds(self, tree, num):
        for elem in tree.findall('node'):
            st = ""
            for n in range(num):
                print("\t", end="")  # 不換行
                st = st + "          "
            print(elem.get('bounds'))
            strstr = st + "(" + str(elem.get('index')) + ") " + str(elem.get('class')) + "  " + str(elem.get('text')) + "  " + str(elem.get('bounds')) + "\n"
            self.XMLTree.insert(END, strstr)
            self.tree_bounds(elem, num + 1)

    def cropImage(self):
        self.canvas = Canvas(self.master, bg='white', width=200, height=200)
        self.canvas.grid(column=self.width + 1, row=35)

    def getmouseEvent(self):
        self.mousePosition = StringVar()  # displays mouse position
        self.mousePosition.set("Mouse outside window")
        self.positionLabel = Label(self.master, textvariable=self.mousePosition)
        self.positionLabel.grid(column=self.width + 1, row=32, columnspan=80)
        self.screenshot.bind("<Button-1>", self.clickdown)  # clickdown
        self.screenshot.bind("<ButtonRelease-1>", self.clickup)  # clickup
        # self.screenshot.bind("<Enter>", self.enteredWindow)
        # self.screenshot.bind("<Leave>", self.exitedWindow)
        self.screenshot.bind("<B1-Motion>", self.mouseDragged)

    def clickdown(self, event):
        self.screenshot.create_image(0, 0, anchor=NW, image=self.screenshot_photo)
        self.mousePosition.set("Pressed at [ " + str(event.x) + ", " + str(event.y) + " ]")

        self.clickstartX = event.x
        self.clickstartY = event.y

    def clickup(self, event):
        self.clickendX = event.x
        self.clickendY = event.y

        left, right = sorted([self.clickendX, self.clickstartX])
        top, bottom = sorted([self.clickstartY, self.clickendY])

        self.cropped = self.photo.crop((left, top, right, bottom))
        #time.sleep(2)
        self.cropped.thumbnail((200, 200))
        #self.cropped.show()
        #
        self.tk_im = ImageTk.PhotoImage(self.cropped)
        self.canvas.create_image(0, 0, anchor=NW,image=self.tk_im)


    #def enteredWindow(self, event):
        #self.mousePosition.set("Mouse in window")

    #def exitedWindow(self, event):
        #self.mousePosition.set("Mouse outside window")

    def mouseDragged(self, event):
        self.screenshot.create_image(0, 0, anchor=NW, image=self.screenshot_photo)
        if event.x < 0 :
            event.x = 0 + 3
        if event.y < 0 :
            event.y = 0 + 3
        if event.x > self.screenshot_photo.width():
            event.x = self.screenshot_photo.width()-3
        if event.y > self.screenshot_photo.height():
            event.y = self.screenshot_photo.height()-3
        self.screenshot.create_rectangle(self.clickstartX, self.clickstartY, event.x, event.y, outline='red' ,width = 2)
        self.mousePosition.set("Rectangle at [ " + str(self.clickstartX * self.resize ) + ", " + str(self.clickstartY * self.resize) + " To " + str(event.x * self.resize) + ", " + str(event.y * self.resize) + " ]")



if __name__ == '__main__':
    root = Tk()
    root.title("Sikuli Viewer")
    app = View(master=root)
    app.mainloop()