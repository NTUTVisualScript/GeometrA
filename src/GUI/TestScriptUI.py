from tkinter import *
from GUI.TestStepUI import TestStepUI

class TestScriptUI(Frame):
    __single = None

    def __init__(self, parent = None, *args, **kwargs):
        if TestScriptUI.__single:
            raise TestScriptUI.__single
            TestScriptUI.__single = self

        Frame.__init__(self, parent, *args, **kwargs, borderwidth =2 ,relief = 'sunken')

        self.canvas = Canvas(self)
        self.listFrame = Frame(self.canvas)

        self.scrollb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollb.pack(side='right', fill='y')
        self.canvas['yscrollcommand'] = self.scrollb.set

        self.canvas.create_window((0, 0), window=self.listFrame, anchor='nw')
        self.listFrame.bind("<Configure>", self.AuxscrollFunction)
        #self.scrollb.grid_forget()

        self.canvas.pack(side="left")
        self.place(x=460, y=300)

        self.scriptstep = TestStepUI()
        n = 0
        for line in range(50):
            self.scriptstep.new_step(self.listFrame, n)
            n += 1


    def getTestScriptUI(parent):
        if not TestScriptUI.__single:
            TestScriptUI.__single = TestScriptUI(parent)
        return TestScriptUI.__single

    def AuxscrollFunction(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=650, height=525)