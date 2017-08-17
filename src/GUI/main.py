import sys
sys.path.append('../')

from tkinter import *
from MenuBar import MenuBar
from ScreenShotUI import ScreenshotUI
from TreeInfoUI import TreeInfoUI
from MessageUI import Message
from TestCaseUI import TestCaseUI


class GUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        master.minsize(width=1470, height=840)
        self.menu = MenuBar.getMenuBar(self.master)
        self.master.config(menu=self.menu)

        self.screenShot = ScreenshotUI.getScreenShotUI(self.master)
        self.treeInfo = TreeInfoUI.getTreeInfoUI(self.master)
        self.testCase = TestCaseUI.getTestCaseUI(self.master)
        self.message = Message.getMessage(self.master)


if __name__ == '__main__':
    root = Tk()
    root.title("Visual Script")
    app = GUI(master=root)
    app.mainloop()
