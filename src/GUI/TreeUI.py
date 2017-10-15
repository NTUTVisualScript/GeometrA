'''
    TreeUI

    Determine all user interface style.
'''

from tkinter import *
class TreeUI(ttk.Treeview):
    def __init__(self, parent=None):
        self.yScrollbar = Scrollbar(parent, orient=VERTICAL)
        self.xScrollbar = Scrollbar(parent, orient=HORIZONTAL)
        super().__init__(parent, yscrollcommand=self.yScrollbar.set, xscrollcommand=self.xScrollbar.set)

        self.column('#0', stretch=YES, minwidth=0, width=350)
        self.place(x = 460, y= 30)
        self["columns"] = ("one", "two")
        self.column("one", width=150)
        self.heading("one", text="Text")
        self.column("two", width=150)
        self.heading("two", text="Bounding Box")

        self.yScrollbar.config(command=self.yview)
        self.xScrollbar.config(command=self.xview)

        self.bind("<ButtonRelease-1>", self.selectNode)
