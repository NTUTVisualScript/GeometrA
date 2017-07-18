from tkinter import *
from tkinter import messagebox
from TestCaseActionCombobox import TestCaseAction
from TestCaseEntry import TestCaseValue

class TestStep():
    def __init__(self, n):
        self.n = Label(self.listFrame, text = str(n+1) + '. ', width = 3)

        self.add = Button(self.listFrame, command=lambda :self.addLineButtonClick(n, False), text = '+', width = 3)
        self.remove = Button(self.listFrame, command=lambda :self.removeLineButtonClick(n, False), text = '-', width = 3)
        self.run = Button(self.listFrame, command=lambda :self.runActionButtonClick(n), text = '▶', width = 3)

        self.actionMenu = TestCaseAction(self.listFrame, textvariable=StringVar(), width=10, height=22, state = 'readonly')
        self.actionMenu.bind('<<ComboboxSelected>>', lambda event, i = n:self.ActionSelect(event, i))
        self.actionMenu.bind('MouseWheel', lambda event, i = n:self.ActionSelect(event, i))

        self.value = TestCaseValue(self.listFrame, width = 35)
        self.value.bind('<FocusIn>', lambda event, i = n: self.valueFocusIn(event, i))

        self.showimage = Button(self.listFrame, command=lambda: self.showImageButtonClick(n), text="show image", width=12)
