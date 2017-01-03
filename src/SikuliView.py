from tkinter import *
from tkinter.filedialog import asksaveasfile, asksaveasfilename

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

ImageType = [
    ('PNG', '*.png'),
    ('JPEG / JPG', '*.jpg'),
    ]

class View(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.formatButton()
        self.ScreenShotUI()
        self.XMLTreeUI()
        self.SaveIMGButton()
        self.cropImage()
        self.getmouseEvent()

    def formatButton(self):
        self.dumpUI = Button(self.master, command=self.formatButtonClick, text="Dump UI")
        self.dumpUI.grid(row=0, column=0, rowspan=2, columnspan = 5)

    def formatButtonClick(self):
        self.getScreenShot()
        self.clear_XML_Tree()
        self.getXMLTree()


    def ScreenShotUI(self):
        self.screenshot = Canvas(self.master, bg='white', height=800, width=450)
        self.screenshot.grid(row=3, column=0, rowspan=50, columnspan = 25)

    def getScreenShot(self):
        self.photo = Image.open(Get_PhoneScreen())
        self.photo_width, self.photo_height = self.photo.size
        print(str(self.photo_width) + " , " + str(self.photo_height))
        self.photo.thumbnail((450, 800))
        self.width, self.height = self.photo.size
        self.resize = self.photo_width / self.width
        print(str(self.resize))
        self.screenshot_photo = ImageTk.PhotoImage(self.photo)
        self.screenshot.create_image(0, 0, anchor=NW, image=self.screenshot_photo)

    def XMLTreeUI(self):
        self.XMLTree = Listbox(self.master, height=15, width=80)
        self.XMLTree.grid(column=25 + 1, row=3, rowspan=15, columnspan=20)

        self.vertscroll = Scrollbar(self.master, orient=VERTICAL)
        self.vertscroll.config(command=self.XMLTree.yview)
        self.vertscroll.grid(column=25 + 22, row=3, rowspan=15, columnspan=1, sticky='NS')

        self.Xvertscroll = Scrollbar(self.master, orient=HORIZONTAL)
        self.Xvertscroll.config(command=self.XMLTree.xview)
        self.Xvertscroll.grid(column=25 + 1, row=18, rowspan=1, columnspan=20, sticky='WE')

        self.XMLTree.config(yscrollcommand=self.vertscroll.set)
        self.XMLTree.config(xscrollcommand=self.Xvertscroll.set)

    def getXMLTree(self):
        self.tree = ET.ElementTree(file = Dump_UI())
        self.tree_bounds(self.tree, 0)

    def clear_XML_Tree(self):
        self.XMLTree.delete( 0 , END )  #clear List box

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

    def SaveIMGButton(self):
        self.SaveIMG = Button(self.master, command=self.SaveIMGButtonClick, text="Save Crop Image")
        self.SaveIMG.grid(row=21, column=26, rowspan=3, columnspan=5)

    def SaveIMGButtonClick(self):
        fileName = asksaveasfilename(initialdir = "/", filetypes=ImageType,title="Save the crop image as...")
        saveIMG = Image.open(filePath)
        left = self.left * self.resize
        top = self.top * self.resize
        right = self.right * self.resize
        bottom = self.bottom * self.resize
        print (str(left) + "\n" + str(top) + "\n" + str(right) + "\n" + str(bottom) )
        cropIMG = saveIMG.crop(( left , top, right, bottom))
        print(fileName)
        savePath = fileName + ".png"
        cropIMG.save(savePath)

    def cropImage(self):
        self.canvas = Canvas(self.master, bg='white', width=200, height=200)
        self.canvas.grid(column=25 + 1, row=24)

    def getmouseEvent(self):
        self.mousePosition = StringVar()  # displays mouse position
        self.mousePosition.set("Mouse outside window")
        self.positionLabel = Label(self.master, textvariable=self.mousePosition)
        self.positionLabel.grid(column=25 + 1, row=20, columnspan=20)
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

        self.left, self.right = sorted([self.clickendX, self.clickstartX])
        self.top, self.bottom = sorted([self.clickstartY, self.clickendY])

        self.cropped = self.photo.crop((self.left, self.top, self.right, self.bottom))
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