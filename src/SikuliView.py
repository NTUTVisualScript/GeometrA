from tkinter import *
from DumpXML import dumpXML
from SaveIMG import saveImg
from DumpScreenShot import dumpScreenShot
from PIL import Image, ImageTk
import os

ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources/taipeibus")

def IMG_PATH(name):
    return os.path.join(RESOURCES_DIR, name)



class View(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.formatButton()

        self.treeUI = dumpXML(self.master)
        self.screenshotUI = dumpScreenShot(self.master)
        self.savecropImg = saveImg()

        self.screenshotUI.ScreenShotUI()
        self.treeUI.XMLTreeUI()


        self.SaveIMGButton()
        self.cropImageUI()
        self.screenshotUI.getmouseEvent()

    def formatButton(self):
        self.dumpUI = Button(self.master, command=self.formatButtonClick, text="Dump UI")
        self.dumpUI.grid(row=0, column=0, rowspan=2, columnspan = 5)

    def formatButtonClick(self):
        self.screenshotUI.getScreenShot()
        self.treeUI.clear_XML_Tree()
        self.treeUI.Tree_infomation()

    def SaveIMGButton(self):
        self.SaveIMG = Button(self.master, command=self.SaveIMGButtonClick, text="Save Crop Image")
        self.SaveIMG.grid(row=0, column=6, rowspan=3, columnspan=8)

    def SaveIMGButtonClick(self):
        self.savecropImg.Save(self.screenshotUI.getImgPath(), self.screenshotUI.getCropRange())

    def cropImageUI(self):
        self.crop = Canvas(self.master, bg='white', width=200, height=200)
        self.crop.grid(column=25 + 1, row=24)


if __name__ == '__main__':
    root = Tk()
    root.title("Sikuli Viewer")
    app = View(master=root)
    app.mainloop()