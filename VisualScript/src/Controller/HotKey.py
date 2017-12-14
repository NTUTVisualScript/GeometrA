from FileLoader import FileLoader
from TestCaseUI import TestCaseUI

class HotKey:
    __single = None
    def __init__(self, parent):
        if HotKey.__single:
            raise HotKey.__single
        self.ctrl_s(parent)
        self.ctrl_r(parent)
        self.ctrl_z(parent)
        self.ctrl_y(parent)

    def getHotKey(parent=None):
        if HotKey.__single is None:
            HotKey.__single = HotKey(parent)
        return HotKey.__single

    def ctrl_s(self, parent):
        parent.bind('<Control-s>', FileLoader.getFileLoader().saveButtonClick)

    def ctrl_r(self, parent):
        parent.bind('<Control-r>', FileLoader.getFileLoader().loadButtonClick)

    def ctrl_z(self, parent):
        parent.bind('<Control-z>', TestCaseUI.getTestCaseUI().ctrl.undoClick)

    def ctrl_y(self, parent):
        parent.bind('<Control-y>', TestCaseUI.getTestCaseUI().ctrl.redoClick)
