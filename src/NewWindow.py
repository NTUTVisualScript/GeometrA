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
from TestCaseButton import TestCaseButton
from FileLoader import FileLoader
from HotKey import HotKey
from MessageUI import Message
from DumpButton import DumpButton
from TreeController import Tree

class Window(View):
    def __init__(self, master=None):
        super().__init__(master)
        TestCaseUI.getTestCaseUI()
        DumpButton(master)
        ScreenshotUI.getScreenshotUI()
        Tree.getTree(master)
        TestCaseButton.getTestCaseButton(master)
        Toolbar.getToolbar(master)
        HotKey.getHotKey(master)
        Message.getMessage(master)
