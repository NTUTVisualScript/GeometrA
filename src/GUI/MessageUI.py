from tkinter import *
import webbrowser
import os

class MessageUI(Text):
    def __init__(self, parent=None):
        Text.__init__(self, parent, bg='white', height=35, width=33, font=('Helvetica', 12), cursor='arrow')
        self.place(x = 1150, y = 30)

        self.scrollb = Scrollbar(parent, orient="vertical", command=self.yview)
        self.scrollb.pack(side='right', fill='y')
        self['yscrollcommand'] = self.scrollb.set

class Message(MessageUI):
    __single = None

    def __init__(self, parent=None):
        MessageUI.__init__(self, parent)
        if Message.__single:
            raise Message.__single
        self.reset()

    def getMessage(parent=None):
        if not Message.__single:
            Message.__single = Message(parent)
        return Message.__single

    def InsertText(self, insertStr, tag=None):
        self.config(state = NORMAL)
        if not tag:
            self.insert('end', insertStr)
        else:
            self.insert('end', insertStr, tag)
        self.insert('end', '\n')
        self.see('end')
        self.config(state = DISABLED)

    def HyperLink(self,insertStr):
        self.tag_config("reportpath", foreground="blue", underline = True)
        self.tag_bind("reportpath", "<Button-1>", lambda e: self.HyperLinkClick(e, insertStr))
        self.config(state = NORMAL)
        self.insert(END, insertStr, "reportpath")
        self.config(state = DISABLED)

    def HyperLinkClick(self, event, insertStr):
        webbrowser.open_new(r"" + insertStr)

    def reset(self):
        self.config(state = NORMAL)
        self.delete(1.0,END)
        title = 'Message Log:'
        self.configure(font=("Times New Roman", 16))
        self.InsertText(title)
        self.config(state = DISABLED)

    def noDevice(self):
        self.InsertText('Device is not connected. ')

    def capturing(self):
        self.InsertText('Capturing the screen shot...')

    def getScreenShot(self):
        self.InsertText('Get ScreenShot Success. ')

    def fileSaved(self, path):
        if path != '':
            s = 'Saving test case success. \n' + 'Path: '
            self.fileHyperLink(s, path)
        else:
            self.InsertText('Test case is not saved. ')

    def fileLoaded(self, path):
        if path != '':
            s = 'Loading test case success. \n' +'Path: '
            self.fileHyperLink(s, path)
        else:
            self.InsertText('No testCase loaded. ')

    def fileHyperLink(self, s, path):
        self.config(state = NORMAL)
        self.InsertText(s)
        self.InsertText(path, 'filepath')
        self.tag_config("filepath", foreground='blue', underline=True, font=("Helvetica", 10))
        self.tag_bind('filepath', '<Button-1>', lambda e:self.fileHyperLinkClick(e, path))

        self.config(state=DISABLED)

    def fileHyperLinkClick(self, event, path):
        folder = os.path.split(path)[0]
        # print(folder)
        os.startfile(folder)
