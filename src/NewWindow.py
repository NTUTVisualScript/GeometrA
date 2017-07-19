from Window import View


from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class Window(View):
    def __init__(self, master=None):
        super().__init__(master)

    def TestCaseFrame(self):
        self.testCaseBlock = Frame(self.master, borderwidth =2 ,relief = 'sunken')
        self.testCaseBlock.place(x=460, y=300)

        self.canvas = Canvas(self.testCaseBlock)
        self.listFrame = Frame(self.canvas)

        self.scroll = Scrollbar(self.testCaseBlock, orient = 'verticla' , command = self.canvas.yview)
        self.scroll.pack(side = 'right', fill = 'y')
        self.canvas['yscrollcommand'] = self.scroll.set

        self.canvas.create_window((0, 0), window = self.Frame, anchor='nw')
        self.listFrame.bind('<Configure>', self.auxscrollFunction)
        self.scroll.grid_forget()

        self.canvas.pack(side='left')


    def auxscrollFunction(self, event):
        self.canvas.configure(scrollregion = self.canvas.bbox('all'), width = 650, height = 525)
