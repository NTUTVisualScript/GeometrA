from tkinter import *

class Message(Text):
    __single = None

    def __init__(self, parent = None):
        Text.__init__(self, parent , bg='white', height=44, width=33, font=("Helvetica", 12))
        if Message.__single:
            raise Message.__single
            Message.__single = self

    def getMessage(parent):
        if not Message.__single:
            Message.__single = Message(parent)
        return Message.__single

    def InsertText(self, insertStr):
        self.insert('end', insertStr)

    def clear(self):
        self.delete(1.0,END)

