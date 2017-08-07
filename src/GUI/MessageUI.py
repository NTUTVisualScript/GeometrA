from tkinter import *
import webbrowser

class Message(Text):
    __single = None

    def __init__(self, parent = None):
        Text.__init__(self, parent , bg='white', height=44, width=33, font=("Helvetica", 12))
        if Message.__single:
            raise Message.__single
            Message.__single = self
        self.place(x = 1150, y= 30)

    def getMessage(parent):
        if not Message.__single:
            Message.__single = Message(parent)
        return Message.__single

    def InsertText(self, insertStr):
        self.insert('end', insertStr)

    def HyperLink(self,insertStr):
        self.tag_config("filepath", foreground="blue", underline = True)
        self.tag_bind("filepath", "<Button-1>", lambda e: self.HyperLinkClick(e, insertStr))
        self.insert(END, insertStr, "filepath")

    def HyperLinkClick(self, event, insertStr):
        webbrowser.open_new(r"" + insertStr)

    def clear(self):
        self.delete(1.0,END)

