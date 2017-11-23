from tkinter import *
from tkinter import ttk

class Tree(ttk.Treeview):

    def __init__(self, parent = None, *args, **kwargs):
        ttk.Treeview.__init__(self, parent, *args, **kwargs)

        self.tree_obj_image_list = []
        self.tree_obj_list = []

        self.column('#0',text = "Class", stretch=YES, minwidth=0, width=350)
        self["columns"] = ("one", "two")
        self.column("one", width=150)
        self.heading("one", text="Text")
        self.column("two", width=150)
        self.heading("two", text="Bounds")

        self.bind("<ButtonRelease-1>", self.on_tree_select)

    def set_coordinate(self, coordinate_x, coordinate_y):
        self.place(x=coordinate_x, y=coordinate_y)

    def get_coordinate(self):
        x = self.place_info().get('x')
        y = self.place_info().get('y')
        return x, y

