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
from MenuBar import MenuBar
from Toolbar import Toolbar
from ClearButton import ClearButton
from Controller.Mouse import Mouse

class Window(View):
    def __init__(self, master=None):
        super().__init__(master)
        MenuBar.getMenuBar(master)
        TestCaseUI.getTestCaseUI()
        ScreenshotUI.getScreenshotUI()
        Toolbar.getToolbar()
        ClearButton().showResetButton()
        Mouse(master)