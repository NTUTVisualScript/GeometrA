from Viewtest import TestAdepter
import time
class Step:
    def __init__(self, action, value, path):
        self.action = action
        self.value = value
        self.path = path

    def run(self):
        if self.action == "":
            return
        if self.action == "Click":
            self.status = self.ClickImage()
            time.sleep(1)
        elif self.action == "Drag":
            self.status = self.DragValue()
            time.sleep(1)
        elif self.action == "Set Text":
            self.status = self.InputValue()
        elif self.action == "TestCase":
            self.status, count = self.TestCasePath()
            self.count = self.count + count
        elif self.action == "Sleep(s)":
            self.status = self.Sleep()
        elif self.action == "Android Keycode":
            self.status = self.Send_Key_Value()
        elif self.action == "Assert Exist":
            self.ActionStatus = self.ExistsImage()
        elif self.action == "Assert Not Exist":
            self.status = self.ExistsImage()
            if self.status == "Success":
                self.status = "Error"
            else:
                self.status = "Success"

        return self.status
