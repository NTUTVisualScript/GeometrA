from tkinter import *
from tkinter import messagebox

import sys
sys.path.append('./TestScript')

from NewWindow import Window
from FileLoader import FileLoader

if __name__ == '__main__':
    root = Tk()
    root.title("Visual Script")
    app = Window(master=root)
    app.mainloop()
