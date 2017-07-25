import time
class Step:
    def __init__(self):
        self.act = ''
        self.val = ''

    def setAction(self, act):
        actList = ['Click', 'Drag', 'Set Text', 'TestCase', 'Loop Begin', 'Loop End',
                    'Sleep(s)', 'Android Keycode', 'Assert Exist', 'Assert Not Exist']
        if act not in actList:
            raise Exception('Not an action')
        self.act = act

    def setValue(self, value):
        self.val = value

    def getAction(self):
        return self.act

    def getValue(self):
        return self.val
