from tkinter import *
from tkinter.ttk import Separator
from PIL import Image, ImageTk
from Controller.FileLoader import FileLoader
from TestCaseUI import TestCaseUI as UI


class Toolbar(Frame):
    __single = None

    def __init__(self, parent = None, *args, **kwargs):
        if Toolbar.__single:
            raise Toolbar.__single
        Toolbar.__single = self

        self._toolbar = Frame(parent, borderwidth=2, relief='groove')
        self._toolbar.pack(fill=X)

        self.fileloader = FileLoader()
        self.ShowSaveButton()
        self.ShowLoadButton()
        ##SeparateBar
        sep = Separator(self._toolbar, orient=VERTICAL)
        sep.pack(side=LEFT, fill=Y)

        self.ShowUndoButton()
        self.ShowRedoButton()
        ##SeparateBar
        sep = Separator(self._toolbar, orient=VERTICAL)
        sep.pack(side=LEFT, fill=Y)

    def getToolbar(parent = None):
        if not Toolbar.__single:
            Toolbar.__single = Toolbar(parent)
        return Toolbar.__single

    def ShowSaveButton(self):
        save_icon_image = Image.open("./img/icon_Save.PNG")
        save_icon_image.thumbnail((20, 20))
        self.SaveIcon = ImageTk.PhotoImage(save_icon_image)
        _saveButton = Button(self._toolbar, image=self.SaveIcon, command=self.fileloader.getFileLoader().saveButtonClick, relief='flat')
        # _saveButton.bind('<Control-s>', lambda: SaveFile().saveButtonClick)
        _saveButton.pack(side=LEFT)

    def ShowLoadButton(self):
        load_icon_image = Image.open("./img/icon_Load.PNG")
        load_icon_image.thumbnail((20, 20))
        self.LoadIcon = ImageTk.PhotoImage(load_icon_image)
        _loadButton = Button(self._toolbar, image=self.LoadIcon, command=self.fileloader.getFileLoader().loadButtonClick, relief='flat')
        _loadButton.pack(side=LEFT)

    def ShowUndoButton(self):
        undo_icon_image = Image.open("./img/icon_Undo.PNG")
        undo_icon_image.thumbnail((20, 20))
        self.UndoIcon = ImageTk.PhotoImage(undo_icon_image)
        _undoButton = Button(self._toolbar, image=self.UndoIcon, command=UI.getTestCaseUI().ctrl.undoClick, relief='flat')
        _undoButton.pack(side=LEFT)

    def ShowRedoButton(self):
        redo_icon_image = Image.open("./img/icon_Redo.PNG")
        redo_icon_image.thumbnail((20, 20))
        self.RedoIcon = ImageTk.PhotoImage(redo_icon_image)
        _redoButton = Button(self._toolbar, image=self.RedoIcon, command=UI.getTestCaseUI().ctrl.redoClick, relief='flat')
        _redoButton.pack(side=LEFT)
