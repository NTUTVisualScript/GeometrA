import time
class Step:
    def __init__(self):
        self.act = ''
        self.val = ''
        self.status = ''

    def setAction(self, act):
        actList = ['', 'Click', 'Drag', 'Set Text', 'TestCase', 'Loop Begin', 'Loop End',
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

    def setStatus(self, status):
        if (status == 'Success') | (status == 'Failed') | (status == 'Error'):
            self.status = status
            return self.status
        raise Exception('setStatus Function Invalid Used Error')

    def getStatus(self):
        if self.status != '':
            return self.status
        raise Exception('Step Not Executed')
