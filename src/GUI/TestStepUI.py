from tkinter import *
from TestCaseActionCombobox import TestCaseAction
from TestCaseEntry import TestCaseValue

class TestStepUI():
    def new_step(self, parent, n):
        self.parent = parent
        action_value = StringVar()

        lineStr = Label(self.parent, text=str(n + 1) + ". ", width=3)

        addline = Button(self.parent, text="+", width=3)

        removeline = Button(self.parent, text="-", width=3)

        run_single_action = Button(self.parent, text="▶",
                                   width=3)

        actioncombo = TestCaseAction(self.parent, textvariable=action_value, width=10, height=22,
                                     state='readonly')
        #actioncombo.bind("<<ComboboxSelected>>",self.ActionSelect)
        #actioncombo.bind("<MouseWheel>",self.ActionSelect)

        value = TestCaseValue(self.parent, width=35)
        #value.bind("<FocusIn>", lambda event, i=n: self.valueFocusIn(event, i))

        #showimage = Button(self.listFrame, command=lambda: self.ShowimageButtonClick(n), text="show image", width=12)

        lineStr.grid(row=n + 1, column=1)
        addline.grid(row=n + 1, column=2)
        removeline.grid(row=n + 1, column=3)
        run_single_action.grid(row=n + 1, column=4)
        actioncombo.grid(row=n + 1, column=5, padx=(5, 0), pady=(5, 2.5))
        value.grid(row=n + 1, column=6, padx=(5, 0), pady=(5, 2.5))