from tkinter import *


class MenuBar(Menu):
    def __init__(self, master=None):
        Menu.__init__(self, master)
        self.config(menu=self.menubar)

        filemenu = Menu(self.menubar, tearoff=0)
        self.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Save  Test Case as...", command=self.SaveButtonClick)
        filemenu.add_command(label="Open  Test Case as...", command=self.OpenButtonClick)

        actionmenu = Menu(self.menubar, tearoff=0)
        self.add_cascade(label="Action", menu=actionmenu)
        actionmenu.add_command(label="Undo", command=self.undo)
        actionmenu.add_command(label="Redo", command=self.redo)

    def SaveButtonClick(self):
        print("SAVE")
        # Save_File = SaveFile()
        # self.dirpath = Save_File.SaveTestCase(self.actioncombolist, self.valuelist, self.valueImagelist,self.node_path_list)

    def OpenButtonClick(self):
        print("Open")
        #Load_File = LoadFile()