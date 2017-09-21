from TestCaseEntry import TestCaseValue
from tkinter import *

def testCaseImage(stepList, line, image = None):
    from TestCaseUI import TestCaseUI
    valueImage = Canvas(TestCaseUI.getTestCaseUI().listFrame, bg = '#FFFFFF', height = 100, width = 100)
    valueImage.create_image(0, 0, anchor=NW, image=image)
    valueImage.bind('<Button-1>', lambda event, i=line: TestCaseUI.getTestCaseUI().valueFocusIn(i))
    valueImage.image = image
    stepList[line].value.grid_remove()
    stepList[line].value = valueImage
    stepList[line].value.grid(row=line + 1, column=6, padx=(5, 0), pady=(5, 2.5))
    stepList[line].showImage.grid(row=line+1, column=7, padx=(5, 0), pady=(5, 2.5))

def testCaseEntry(stepList, line):
    from TestCaseUI import TestCaseUI
    value = TestCaseValue(TestCaseUI.getTestCaseUI().listFrame, width = 35)
    value.bind('<FocusIn>', lambda event, i = line: TestCaseUI.getTestCaseUI().valueFocusIn(i))
    value.bind('<KeyRelease>', lambda event, i = line: TestCaseUI.getTestCaseUI().valueModified(i))
    stepList[line].value.grid_remove()
    stepList[line].value = value
    stepList[line].value.grid(row=line + 1, column=6, padx=(5, 0), pady=(5, 2.5))
    stepList[line].showImage.grid_remove()
