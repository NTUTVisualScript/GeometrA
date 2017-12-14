class Loop:
    def __init__(self, stepList, n):
        from TestCaseUI import TestCaseUI
        TestCaseUI.getTestCaseUI().addStep(n+1)
        TestCaseUI.getTestCaseUI().addStep(n+2)
        stepList[n+2].action.set('Loop End')


class Swipe:
    def __init__(self):
        self.swipeImage = Canvas(self.screenshot, height=800, width=450)
        self.swipeImage.configure(borderwidth=-3)
        self.swipeImage.place(x=0, y=0)

        self.swipeImage.create_image(0, 0, anchor=NWW, image=self.screenshot_photo)
        self.swipeImage.image = self.screenshot_photo
        self.swipeImage.bind('<Button-1>', self.swipeDown)
        self.swipeImage.bind('<ButtonRelease-1>', self.swipeUp)
        self.swipeImage.bind('<Motion>', self.swipeMotion)
        self.swipeImage.bind('<Enter>', self.swipeEnter)
        self.swipeImage.bind('<B1-Motion>', self.swiped)

    def place_forget(self):
        self.swipeImage.place_forget()

    def swipeDown(self, event):
        self.clickStartX = event.x
        self.clickStartY = event.y

    def swipeUp(self, event):
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

    def swipeEnter(self, event):
        self.focusOBJImage = self.Drag_image.image

    def swiped(self, event):
        self.dragImage.delete('all')
        self.dragImage.create_image(0, 0, anchor=NW, image=self.focusOBJImage)
        self.dragImage.image = self.focusOBJImage

        self.mousePosition.set('Rectangle at [ ' + str(self.clickStartX * self.multiple) + \
                            ', ' + str(self.clickStartY * self.multiple) + ' To ' + \
                            str(event.x * self.multiple) + ', ' + str(event.y * self.multiple) + ' ]')
        self.drawArrow(self.clickStartX, self.clickStartY, event.x, event.y)
