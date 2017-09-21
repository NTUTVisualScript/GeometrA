from Window import View


from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import sys
sys.path.append('./GUI')
sys.path.append('./GUI/TestCase')
sys.path.append('./TestCase')
sys.path.append('./Save')
sys.path.append('./Controller')
from TestCaseUI import TestCaseUI
from ScreenshotUI import ScreenshotUI
from Toolbar import Toolbar
from TestCaseButtons import *


class Window(View):
    def __init__(self, master=None):
        super().__init__(master)
        TestCaseUI.getTestCaseUI()
        ScreenshotUI.getScreenshotUI()
        ClearButton(master).showClearButton()
        Toolbar.getToolbar()
        RunButton(master).showRunButton()
