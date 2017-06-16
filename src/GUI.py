from tkinter import *

class GUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

if __name__ == '__main__':
    root = Tk()
    root.title("Visual Script")
    app = GUI(master=root)
    app.mainloop()