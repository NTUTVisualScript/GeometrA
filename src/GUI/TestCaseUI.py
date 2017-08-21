from tkinter import *
from GUI.TestStepUI import TestStepUI
from TestCaseActionCombobox import TestCaseAction
from TestCaseEntry import TestCaseValue
from LoadFile import LoadFile

import sys
sys.path.append('../TestCase/')
from TestCase import TestCase
from TestStep import Step
from Executor import Executor

filePath = None

class TestCaseUI(Frame):
    __single = None
    case = None

    def __init__(self, parent = None, *args, **kwargs):
        if TestCaseUI.__single:
            raise TestCaseUI.__single
            TestCaseUI.__single = self
        self.case = TestCase()

        Frame.__init__(self, parent, *args, **kwargs, borderwidth =2 ,relief = 'sunken')

        self.canvas = Canvas(self)
        self.listFrame = Frame(self.canvas)

        self.scrollb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollb.pack(side='right', fill='y')
        self.canvas['yscrollcommand'] = self.scrollb.set

        self.canvas.create_window((0, 0), window=self.listFrame, anchor='nw')
        self.listFrame.bind("<Configure>", self.AuxscrollFunction)
        #self.scrollb.grid_forget()

        self.canvas.pack(side="left")
        self.place(x=460, y=300)

        self.swipeImage = None
        self.stepList = []
        for i in range(15):
            step = TestStepUI(self.listFrame, i)
            self.stepList.append(step)


    def getTestCaseUI(parent=None):
        if not TestCaseUI.__single:
            TestCaseUI.__single = TestCaseUI(parent)
        return TestCaseUI.__single

    def AuxscrollFunction(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=650, height=525)

    def addButtonClick(self, n):
        i = len(self.stepList)
        self.stepList.append(TestStepUI(self.listFrame, len(self.stepList)))

        while i > n:
            action = self.stepList[i-1].action.get()
            self.stepList[i].action.set(str(action))
            self.stepList[i-1].action.set('')

            if str(type(self.stepList[i-1].value)) != "<class 'TestCaseEntry.TestCaseValue'>":
                self.testCaseImage(i, self.stepList[i-1].value.image)
                self.testCaseEntry(i-1)
            else:
                value = self.stepList[i-1].value.get()
                self.stepList[i].value.delete(0, 'end')
                self.stepList[i].value.insert('end', value)
                self.stepList[i-1].value.delete(0, 'end')
            i = i-1

    def removeButtonClick(self, n):
        i = n
        while i < len(self.stepList)-1:
            action = self.stepList[i+1].action.get()
            self.stepList[i].action.set(str(action))

            if str(type(self.stepList[i+1].value)) != "<class 'TestCaseEntry.TestCaseValue'>":
                self.testCaseImage(i, self.stepList[i+1].value.image)
                self.testCaseEntry(i+1)
            else:
                self.testCaseEntry(i)
                value = self.stepList[i+1].value.get()
                self.stepList[i].value.delete(0, 'end')
                self.stepList[i].value.insert('end', value)
            i = i+1

        self.stepList[len(self.stepList)-1].remove()
        self.stepList.pop()

    def testCaseImage(self, line, image = None):
        valueImage = Canvas(self.listFrame, bg = '#FFFFFF', height = 100, width = 100)
        valueImage.create_image(0, 0, anchor=NW, image=image)
        valueImage.bind('<Button-1>', lambda event, i=line: self.valueFocusIn(i))
        valueImage.image = image
        self.stepList[line].value.grid_remove()
        self.stepList[line].value = valueImage
        self.stepList[line].value.grid(row=line + 1, column=6, padx=(5, 0), pady=(5, 2.5))

    def testCaseEntry(self, line):
        value = TestCaseValue(self.listFrame, width = 35)
        value.bind('<FocusIn>', lambda event, i = line: self.valueFocusIn(i))
        self.stepList[line].value.grid_remove()
        self.stepList[line].value = value
        self.stepList[line].value.grid(row=line + 1, column=6, padx=(5, 0), pady=(5, 2.5))

    def actionSelect(self, n):
        self.focus = n
        # print(str(self.stepList[n].action.get()))
        self.case.insert(n, Step())
        self.case.setAction(n, self.stepList[n].action.get())
        self.testCaseEntry(n)
        self.actionFocusIn()

    def actionFocusIn(self):
        action = self.stepList[self.focus].action.get()

        if (action != 'Swipe') & (self.swipeImage != None):
            self.swipeImage.place_forget()
            self.swipeImage = None

        if action == 'Swipe':
            if filePath is None: return
            '''
                Swipe could be acceptance after dumpUI and Screenshot are done.
                And here should be modified after they are done.
            '''
            self.swipeImage = Canvas(self.screenshot, height=800, width=450)
            self.swipeImage.configure(borderwidth=-3)
            self.swipeImage.place(x=0, y=0)

            self.swipeImage.create_image(0, 0, anchor=NWW, image=self.screenshot_photo)
            self.swipeImage.image = self.screenshot_photo
            self.swipeIamge.bind('<Button-1>', self.dragDown)
            self.swipeImage.bind('<ButtonRelease-1>', self.dragUp)
            self.swipeImage.bind('<Motion>', self.swipeMotion)
            self.swipeIamge.bind('<Enter>', self.dragEnter)
            self.swipeImage.bind('<B1-Motion>', self.dragged)
        elif action == 'TestCase':
            openfile = LoadFile()
            path = openfile.LoadTestCasePath()
            if (path is not None) and (path != ''):
                self.stepList[self.focus].value.delete(0, 'end')
                self.stepList[self.focus].value.insert('end', path)
        elif action == 'Click' or action == 'Assert Exist' or action == 'Assert Not Exist':
            self.testCaseImage(self.focus)

    def dragDown(self, event):
        self.clickStartX = event.x
        self.clickStartY = event.y

    def dragUp(self, event):
        self.clickEndX = event.x
        self.clickEndY = event.y
        self.left, self.right = sorted([self.clickEndX, self.clickStartX])
        self.top, self.bottom = sorted([self.clickStartY, self.clickEndY])

        if self.left != self.right or self.top != self.bottom:
            if self.stepList[n].action.get() == 'Swipe':
                text = 'start x=' + str(int(self.clickStartX * self.multiple)) + \
                       'start y=' + str(int(self.clickStartY * self.multiple)) + \
                       'end x=' + str(int(self.clickEndX * self.multiple)) + \
                       'end y=' + str(int(self.clickEndY * self.multiple))
                self.stepList[n].value.delete(0, 'end')
                self.valueList[n].value.insert('end', text)

    def swipeMotion(self, event):
        self.mousePosition.set('Mouse in window [ ' + str(int(event.x * self.multiple)) + \
                            ', ' + str(int(event.y * self.multiple)) + ' ]')

    def dragEnter(self, event):
        self.focusOBJImage = self.Drag_image.image

    def dragged(self, event):
        self.dragImage.delete('all')
        self.dragImage.create_image(0, 0, anchor=NW, image=self.focusOBJImage)
        self.dragImage.image = self.focusOBJImage

        self.mousePosition.set('Rectangle at [ ' + str(self.clickStartX * self.multiple) + \
                            ', ' + str(self.clickStartY * self.multiple) + ' To ' + \
                            str(event.x * self.multiple) + ', ' + str(event.y * self.multiple) + ' ]')
        self.drawArrow(self.clickStartX, self.clickStartY, event.x, event.y)
