from tkinter import *
import threading
from ScreenshotUI import ScreenshotUI

class DumpButton:
    def __init__(self, master):
        self.dumpUI = Button(master, command=lambda: threading.Thread(target=self.dump).start(),
                             text="Capture Screenshot", width=18)
        self.dumpUI.place(x=0, y=30)

    def dump(self):
        ScreenshotUI.getScreenshotUI().getScreenshot()
