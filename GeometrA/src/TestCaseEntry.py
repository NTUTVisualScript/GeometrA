from tkinter import *


class TestCaseValue(Entry):
    def __init__(self, parent, *args, **kwargs):
        Entry.__init__(self, parent, *args, **kwargs)
        self.changes = [""]
        self.steps = int()
        self['font'] = ('Times', 13, 'bold italic')
        self.bind("<Control-z>", self.undo)
        self.bind("<Control-y>", self.redo)
        self.bind("<Key>", self.add_changes)

    def undo(self, event=None):
        if self.steps != 0:
            self.steps -= 1
            self.delete(0, END)
            self.insert(END, self.changes[self.steps])

    def redo(self, event=None):
        if self.steps < len(self.changes):
            self.delete(0, END)
            self.insert(END, self.changes[self.steps])
            self.steps += 1

    def add_changes(self, event=None):
        if self.get() != self.changes[-1]:
            self.changes.append(self.get())
            self.steps += 1
