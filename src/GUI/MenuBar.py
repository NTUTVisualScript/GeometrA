from tkinter import *
# from Save.Load.py import FileLoader
# from Save.Save import Save

class MenuBar(Menu):
    __single = None

    def __init__(self, parent = None):
        if MenuBar.__single:
            raise MenuBar.__single
        MenuBar.__single = self

        self.menubar = Menu.__init__(self, parent)
        self.config(menu=self.menubar)

        filemenu = Menu(self.menubar, tearoff=0)
        self.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Save Test Case as...", command=self.SaveButtonClick)
        filemenu.add_command(label="Open Test Case", command=self.OpenButtonClick)

        actionmenu = Menu(self.menubar, tearoff=0)
        self.add_cascade(label="Action", menu=actionmenu)
        actionmenu.add_command(label="Undo", command=self.undo)
        actionmenu.add_command(label="Redo", command=self.redo)

    def getMenuBar(parent = None):
        if not MenuBar.__single:
            MenuBar.__single = MenuBar(parent)
        return MenuBar.__single

    def SaveButtonClick(self):
        print("SAVE")
        #Save_File = Save()
        #self.dirpath = Save_File.SaveTestCase(self.actioncombolist, self.valuelist, self.valueImagelist,self.node_path_list)

    def OpenButtonClick(self):
        print("Open")
        #Load_File = LoadFile()

    def redo(self):
        print("Redo")

    def undo(self):
        print("Undo")