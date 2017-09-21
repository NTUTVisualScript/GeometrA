import time
from AndroidKeycode import AndroidKeycode as key

class Step:
    def __init__(self, act, val, node=None):
        self.act = ''
        self.val = ''
        self.setAction(act)
        self.setValue(val)
        '''
        Node part have to wait for Tree_Info Design
        '''
        self.setNode(node)
        self.status = 'Not Executed'

    def setStep(self, act, val, node=None):
        self.setAction(act)
        self.setValue(val)
        self.setNode(node)

    def setAction(self, act):
        if self.act == act:
            return
        actList = ['', 'Click', 'Swipe', 'Set Text', 'TestCase', 'Loop Begin', 'Loop End',
                    'Sleep(s)', 'Android Keycode', 'Assert Exist', 'Assert Not Exist']
        if act not in actList:
            raise Exception('Not an action')
        self.act = act

    def setNode(self, node):
        self.node = node

    def setValue(self, value):
        if (self.act == 'Click') or (self.act == 'Assert Exist') or (self.act == 'Assert Not Exist'):
            if (str(value.__class__) != "<class 'PIL.PngImagePlugin.PngImageFile'>") \
                    and (str(value.__class__) != "<class 'PIL.Image.Image'>"):
                raise Exception('Value Should be PIL image')
        if ((self.act == 'Sleep(s)') or (self.act == 'Loop Begin')) and (not value.isdigit()):
            raise Exception('Value Should be digit')
        if self.act == 'Android Keycode':
            if value.isdigit():
                try:
                    key[int(value)]
                except:
                    raise Exception('Value is not Android Keycode')
            elif not(value in list(key.values())):
                raise Exception('Value is not Android Keycode')

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
        if self.status != 'Not Executed':
            return self.status
        raise Exception('Step Not Executed')
