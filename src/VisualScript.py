from tkinter import *
from tkinter import messagebox

import sys
sys.path.append('./TestCase')

from Window import View
from NewWindow import Window

if __name__ == '__main__':
    root = Tk()
    root.title("Visual Script")
    app = Window(master=root)
    app.mainloop()
