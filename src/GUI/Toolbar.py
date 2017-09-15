from tkinter import *
from tkinter.ttk import Separator
from PIL import Image, ImageTk
from Controller.FileLoader import SaveFile, LoadFile

class Toolbar(Frame):
    __single = None

    def __init__(self, parent = None, *args, **kwargs):
        if Toolbar.__single:
            raise Toolbar.__single
        Toolbar.__single = self

        self._toolbar = Frame(parent, borderwidth=2, relief='groove')
        self._toolbar.pack(fill=X)

        self.SaveButton()
        self.LoadButton()
        sep = Separator(self._toolbar, orient=VERTICAL)
        sep.pack(side=LEFT, fill=Y)

    def getToolbar(parent = None):
        if not Toolbar.__single:
            Toolbar.__single = Toolbar(parent)
        return Toolbar.__single

    def SaveButton(self):
        save_icon_image = Image.open("./img/icon_Save.PNG")
        save_icon_image.thumbnail((20, 20))
        self.SaveIcon = ImageTk.PhotoImage(save_icon_image)
        _saveButton = Button(self._toolbar, image=self.SaveIcon, command=SaveFile(), relief='flat')
        _saveButton.pack(side=LEFT)

    def LoadButton(self):
        load_icon_image = Image.open("./img/icon_Load.PNG")
        load_icon_image.thumbnail((20, 20))
        self.LoadIcon = ImageTk.PhotoImage(load_icon_image)
        _loadButton = Button(self._toolbar, image=self.LoadIcon, command=LoadFile().loadPath, relief='flat')
        _loadButton.pack(side=LEFT)