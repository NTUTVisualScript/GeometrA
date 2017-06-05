from tkinter import *
from TestCaseActionCombobox import TestCaseAction
from TestCaseEntry import TestCaseValue
from LoadFile import LoadFile

class TestCaseFrame(Frame):
    __single = None

    def __init__(self, parent = None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        if TestCaseFrame.__single:
            raise TestCaseFrame.__single
            TestCaseFrame.__single = self

        self.canvas = Canvas(self.frameTwo)
        self.listFrame = Frame(self.canvas)

        self.scrollb = Scrollbar(self.frameTwo, orient="vertical", command=self.canvas.yview)
        self.scrollb.pack(side='right', fill='y')
        self.canvas['yscrollcommand'] = self.scrollb.set

        self.canvas.create_window((0, 0), window=self.listFrame, anchor='nw')
        self.listFrame.bind("<Configure>", self.AuxscrollFunction)
        self.scrollb.grid_forget()

        self.canvas.pack(side="left")

        self.lineStrlist = []
        self.addlinelist = []
        self.removelinelist = []
        self.run_single_actionlist = []
        self.actioncombolist = []
        self.valuelist = []
        self.showimagelist = []
        self.valueImagelist = []
        self.node_path_list = []

        n = 0
        for self.line in range(50):
            self.new_line(n)
            n = n + 1

    def getTestCaseFrame(parent):
        if not TestCaseFrame.__single:
            TestCaseFrame.__single = TestCaseFrame(parent)
        return TestCaseFrame.__single

    def AuxscrollFunction(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=650, height=525)

    def new_line(self,n):
        action_value = StringVar()

        lineStr = Label(self.listFrame, text=str(n+1)+". ", width=3)
        self.lineStrlist.append(lineStr)
        addline = Button(self.listFrame, command=lambda:self.AddLineButtonClick(n), text="+", width=3)
        self.addlinelist.append(addline)

        removeline = Button(self.listFrame, command=lambda:self.RemoveLineButtonClick(n), text="-", width=3)
        self.removelinelist.append(removeline)

        run_single_action = Button(self.listFrame, command=lambda: self.Run_single_actionButtonClick(n), text="▶", width=3)
        self.run_single_actionlist.append(run_single_action)

        actioncombo = TestCaseAction(self.listFrame, textvariable=action_value, width=10, height=22,
                                   state='readonly')
        actioncombo.bind("<<ComboboxSelected>>", lambda event, i=n: self.ActionSelect(event, i))
        actioncombo.bind("<MouseWheel>", lambda event, i=n: self.ActionSelect(event, i))
        self.actioncombolist.append(actioncombo)

        value = TestCaseValue(self.listFrame,width=35)
        value.bind("<FocusIn>", lambda event, i=n: self.valueFocusIn(event, i))

        showimage = Button(self.listFrame, command=lambda: self.ShowimageButtonClick(n), text="show image", width=12)
        self.showimagelist.append(showimage)

        self.valuelist.append(value)
        self.valueImagelist.append(None)
        self.node_path_list.append(None)

        lineStr.grid(row = n+1 , column = 1 )
        addline.grid(row = n+1 , column = 2 )
        removeline.grid(row=n+1, column=3)
        run_single_action.grid(row=n+1, column=4)
        actioncombo.grid(row = n+1 , column = 5 , padx = ( 5 , 0 ) , pady = ( 5 , 2.5))
        value.grid(row = n+1 , column = 6 , padx = ( 5, 0) , pady = ( 5 , 2.5))

    def ActionSelect(self,event, n):
        self.focus = n
        #self.cmd.do(self.actioncombolist[n])
        self.valueImagelist[n] = None
        self.TestcaseEntry(n)
        self.Action_FocusIn()

    def valueFocusIn(self,event, n):
        self.focus = n

    def Action_FocusIn(self):
        if self.actioncombolist[self.focus].get() == 'Drag':
            self.Drag_image = Canvas(self.screenshot, height=800, width=450)
            self.Drag_image.configure(borderwidth=-3)
            self.Drag_image.place(x=0, y=0)

            self.Drag_image.create_image(0, 0, anchor=NW, image=self.screenshot_photo)
            self.Drag_image.image = self.screenshot_photo
            self.Drag_image.bind("<Button-1>", self.Dragdown)  # clickdown
            self.Drag_image.bind("<ButtonRelease-1>", self.Dragup)  # clickup
            self.Drag_image.bind("<Motion>", self.Dragmotion)  # get mouse coordination
            self.Drag_image.bind("<Enter>", self.DragEnter)
            self.Drag_image.bind("<B1-Motion>", self.Dragged)  # 滑鼠拖拉動作
        elif self.actioncombolist[self.focus].get() == 'TestCase':
            openfile = LoadFile()
            path = openfile.LoadTestCasePath()
            if path is not None:
                if path !="":
                    self.valuelist[self.focus].delete(0, 'end')
                    self.valuelist[self.focus].insert('end', path)
        else:
            if self.Drag_image != None:
                self.Drag_image.place_forget()
                self.Drag_image = None

    def Dragdown(self, event):
        self.clickstartX = event.x
        self.clickstartY = event.y

    def Dragup(self, event):
        self.clickendX = event.x
        self.clickendY = event.y
        self.left, self.right = sorted([self.clickendX, self.clickstartX])
        self.top, self.bottom = sorted([self.clickstartY, self.clickendY])

        if self.left != self.right or self.top != self.bottom:
                if self.actioncombolist[self.focus].get() == 'Drag':
                    text = "start x=" + str(int(self.clickstartX * self.multiple)) + ", y=" + str(int(self.clickstartY * self.multiple)) + " , " +\
                           "end x=" + str(int(self.clickendX * self.multiple)) + ", y=" + str(int(self.clickendY * self.multiple))
                    self.valuelist[self.focus].delete(0, 'end')
                    self.valuelist[self.focus].insert('end', text)

    def Dragmotion(self,event):
        self.mousePosition.set("Mouse in window [ " + str(int((event.x) * self.multiple)) + ", " + str(int((event.y) * self.multiple)) + " ]")

    def DragEnter(self, event):
        self.focusOBJImage = self.Drag_image.image

    def Dragged(self, event):
        self.Drag_image.delete("all")
        self.Drag_image.create_image(0, 0, anchor=NW, image=self.focusOBJImage)
        self.Drag_image.image = self.focusOBJImage

        self.mousePosition.set("Rectangle at [ " + str(self.clickstartX * self.multiple ) + ", " + str(self.clickstartY * self.multiple) + " To " + str((event.x) * self.multiple) + ", " + str((event.y) * self.multiple) + " ]")
        self.Drag_image.create_line(self.clickstartX, self.clickstartY, event.x, event.y, fill="red", width=2)