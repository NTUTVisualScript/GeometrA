from tkinter import *
from tkinter import ttk

class TestCaseAction(ttk.Combobox):
    def __init__(self, parent, n, *args, **kwargs):
        ttk.Combobox.__init__(self, parent, *args, **kwargs)
        self['values'] = (
        '', 'Click', 'Drag', 'Set Text', 'TestCase', 'Loop Begin', 'Loop End', 'Sleep(s)', 'Android Keycode', 'Assert Exist',
        'Assert Not Exist')
        self['font'] = ('Times', 11, 'bold italic')
        self.current(n)
        # self.bind("<<ComboboxSelected>>", self.ActionSelect)
        # self.bind("<MouseWheel>",  self.ActionSelect)
