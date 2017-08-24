from Window import View


from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import sys
sys.path.append('./GUI')
sys.path.append('./TestCase')
sys.path.append('./Save')
from TestCaseUI import TestCaseUI

class Window(View):
    def __init__(self, master=None):
        super().__init__(master)
        TestCaseUI.getTestCaseUI()
