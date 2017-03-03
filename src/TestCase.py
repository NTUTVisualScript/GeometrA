from tkinter import *
from tkinter import ttk

class TestCase(Frame):

    def view(self):
        self.frameTwo = Frame(self.master,width=650, height=600)
        self.frameTwo.place(x=460, y=300)

        self.create_cells()

    def create_cells(self):
        """Create cells for exception text"""
        # ----------------------------------------------
        frame_fieldsscroll = Text(self.frameTwo, relief='flat')
        text_fields = Text(frame_fieldsscroll, relief='flat', width = 90)
        frame_fieldsscroll.window_create('insert', window=text_fields)

        tf = {}
        for f in range(31):
            self.action_value = StringVar()
            self.type_value = StringVar()
            actioncombo = ttk.Combobox(self.frameTwo, textvariable=self.action_value,width=15,height=22,
                                state='readonly')
            actioncombo['values'] = ('','Click', 'Drag', 'Assert')
            actioncombo.current(0)

            typecombo = ttk.Combobox(self.frameTwo, textvariable=self.type_value, width=15,height=22,
                                      state='readonly')
            typecombo['values'] = ('','Image', 'coordinate')
            typecombo.current(0)

            value = Text(text_fields,height=1, width=52)

            actioncombo.place(x = 0,y = 0 + (50*f-1))
            typecombo.place(x = 0+(150*f-1),y = 0 + (50*f-1) )
            value.place(x=0 + (300 * f - 1), y=0 + (50*f-1))

            text_fields.window_create('insert', window=actioncombo)
            text_fields.window_create('insert', window=typecombo)
            text_fields.window_create('insert', window=value)

            text_fields.insert('end', '\n')

        scrollbar = Scrollbar(frame_fieldsscroll, width=15)
        scrollbar.config(command=text_fields.yview)
        text_fields.config(yscrollcommand=scrollbar.set)

        frame_fieldsscroll.pack()
        scrollbar.pack(side='right', fill='y')
        text_fields.pack(fill='both')

        text_fields.configure(state='disabled')
        frame_fieldsscroll.configure(state='disabled')



        # self.testcase = ttk.Treeview(self.frameTwo, height =25)
        # self.testcase["columns"] = ("one", "two")
        # self.testcase.column('#0', stretch=YES, minwidth=0, width=150)
        # self.testcase.heading('#0', text="Action")
        # self.testcase.column("one", width=150)
        # self.testcase.heading("one", text="Type")
        # self.testcase.column("two", width=350)
        # self.testcase.heading("two", text="Value")
        # self.testcase.place(x = 0, y = 0)

        #self.box = StringVar(ActionCombo(self.frameTwo))
        #self.testcase.insert("",0,text = self.box )




