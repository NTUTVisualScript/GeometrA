from TestStepUI import TestStepUI

class TestCaseUI():
    def __init__(self, frame):
        self.frame = frame
        self.case = TestCase(50)
        self.addButtonList = []
        self.removeButtonList = []
        self.executeButtonList = []
        self.actionMenuList = []
        self.valueBar = []

        self.generateCaseBlock()

    # To generate the block on the UI for Test Case
    def generateCaseBlock():
        n = self.case.stepSize

        # Generate one line at one time
        for i in range(0, n):
            Label(self.listFrame, text = str(i+1) + '. ', width = 3)
            self.addButtonList.append(Button(self.frame, command=lambda: self.addButtonClick(i, False), text='+', width=3))
            self.removeButtonList.append(Button(self.frame, command=lambda: self.removeButtonClick(i, False), text='-', width=3))
            self.executeButtonList.append(Button(self.frame, command=lambda: self.executeButtonClick(i, False), text='▶', width=3))

            self.actionMenuList.append(TestCaseAction(self.frame, textvariable=StringVar(), width=10, height=22, state='readonly'))
            self.actionMenuList[i].bind('<<ComboboxSelected>>', lambda event, j=i: self.actionSelect(event, i))
            self.actionMenuList[i].bind('<MouseWheel>', lambda event, j=i: self.actionSelect(event, i))


    def actionSelect(self, event, n):
        self.focus = n
