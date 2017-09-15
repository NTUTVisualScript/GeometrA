from tkinter import *
from PIL import Image, ImageTk
from Controller.FileLoader import SaveFile, LoadFile

class Toolbar(Frame):
    __single = None

    def __init__(self, parent = None, *args, **kwargs):
        if Toolbar.__single:
            raise Toolbar.__single
        Toolbar.__single = self

        _toolbar = Frame(parent, borderwidth=2, relief='groove')
        _toolbar.pack(fill=X)
        self._saveIcon = Image.open("./img/icon_Save.PNG")
        self._saveIcon.thumbnail((20, 20))
        self.SaveIcon = ImageTk.PhotoImage(self._saveIcon)
        self.SaveButton = Button(_toolbar, image=self.SaveIcon, command=SaveFile(), relief='flat')
        self.SaveButton.pack(side=LEFT)

        self._loadIcon = Image.open("./img/icon_Load.PNG")
        self._loadIcon.thumbnail((20, 20))
        self.LoadIcon = ImageTk.PhotoImage(self._loadIcon)
        self.LoadButton = Button(_toolbar, image=self.LoadIcon, command=LoadFile().loadPath, relief='flat')
        self.LoadButton.pack(side=LEFT)


    def getToolbar(parent = None):
        if not Toolbar.__single:
            Toolbar.__single = Toolbar(parent)
        return Toolbar.__single

