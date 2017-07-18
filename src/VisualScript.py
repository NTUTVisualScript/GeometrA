from tkinter import *
from tkinter import messagebox

from Window import View

if __name__ == '__main__':
    root = Tk()
    root.title("Visual Script")
    app = View(master=root)
    app.mainloop()
