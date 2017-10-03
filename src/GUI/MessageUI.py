from tkinter import *
import webbrowser

class Message(Text):
    __single = None

    def __init__(self, parent=None):
        Text.__init__(self, parent, bg='white', height=35, width=33, font=("Helvetica", 12))
        if Message.__single:
            raise Message.__single
        self.place(x = 1150, y= 30)
        self.reset()
        self.config(state = DISABLED)

    def getMessage(parent=None):
        if not Message.__single:
            Message.__single = Message(parent)
        return Message.__single

    def InsertText(self, insertStr):
        self.config(state = NORMAL)
        self.insert('end', insertStr)
        self.insert('end', '\n')
        self.config(state = DISABLED)

    def HyperLink(self,insertStr):
        self.tag_config("filepath", foreground="blue", underline = True)
        self.tag_bind("filepath", "<Button-1>", lambda e: self.HyperLinkClick(e, insertStr))
        self.insert(END, insertStr, "filepath")

    def HyperLinkClick(self, event, insertStr):
        webbrowser.open_new(r"" + insertStr)

    def reset(self):
        self.delete(1.0,END)
        title = 'Message Log:'
        self.configure(font=("Times New Roman", 16))
        self.InsertText(title)
