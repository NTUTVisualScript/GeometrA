from tkinter import *
from tkinter import ttk
from Viewtest import TestAdepter

class TestCaseFrame(Frame):
    def view(self):
        self.frameTwo = Frame(self.master,width=450, height=300)
        self.frameTwo.place(x=460, y=300)
        self.frame_fieldsscroll = Text(self.frameTwo, relief='flat')
        self.text_fields = Text(self.frame_fieldsscroll, relief='flat', width=70)
        self.text_fields['font'] = ('Times', 18, 'bold italic')
        self.frame_fieldsscroll.window_create('insert', window=self.text_fields)

        scrollbar = Scrollbar(self.frame_fieldsscroll, width=15)
        scrollbar.config(command=self.text_fields.yview)
        self.text_fields.config(yscrollcommand=scrollbar.set)

        self.frame_fieldsscroll.pack()
        scrollbar.pack(side='right', fill='y')
        self.text_fields.pack(fill='both')

        self.text_fields.configure(state='disabled')
        self.frame_fieldsscroll.configure(state='disabled')

class TestCase(TestCaseFrame):
    def create_cells(self):
        self.actioncombolist = []
        self.typecombolist = []
        self.valuelist = []
        self.action_value = StringVar()
        self.type_value = StringVar()
        for line in range(30):
            self.new_line()

    def new_line_buttonClick(self):
        self.new_line()

    def RunTest(self):
        run = TestAdepter()
        run.Test(self.actioncombolist,self.typecombolist,self.valuelist)

    def new_line(self):

        actioncombo = ttk.Combobox(self.frameTwo, textvariable=self.action_value, width=15, height=22,
                                   state='readonly')
        actioncombo['values'] = ('', 'Click', 'Drag', 'Assert')
        actioncombo['font'] = ('Times', 13, 'bold italic')
        actioncombo.bind("<<>ComboboxSelected>")
        actioncombo.current(0)
        self.actioncombolist.append(actioncombo)

        typecombo = ttk.Combobox(self.frameTwo, textvariable=self.type_value, width=15, height=22,
                                 state='readonly')
        typecombo['values'] = ('', 'image', 'coordinate')
        typecombo['font'] = ('Times', 13, 'bold italic')
        typecombo.bind("<<>ComboboxSelected>")
        typecombo.current(0)
        self.typecombolist.append(typecombo)

        value = Text(self.text_fields, height=1, width=52)
        value['font'] = ('Times', 15, 'bold italic')

        actioncombo.pack()
        typecombo.pack()
        value.pack()

        self.text_fields.window_create('insert', window=actioncombo)
        self.text_fields.window_create('insert', window=typecombo)
        self.text_fields.window_create('insert', window=value)

        self.text_fields.insert('end', '\n')





