class Undo:
    def __init__(self, case):
        self.userAction = []
        self.case = case.copy()
        self.userAction.append(self.case)

    def push(self, case):
        self.userAction.append(case.copy())
        if len(self.userAction) > 5:
            self.userAction.pop(0)

    def pop(self):
        case = self.userAction.pop()
        if len(self.userAction) == 0:
            self.userAction.append(self.case)
        return case

class Redo:
    def __init__(self):
        self.action = []

    def push(self, case):
        self.action.append(case.copy())

    def pop(self):
        return self.action.pop()

    def reset(self):
        del self.action
        self.action = []

    def getSize(self):
        return len(self.action)
