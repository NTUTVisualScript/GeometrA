class Undo:
    def __init__(self, case):
        self.userAction = []
        self.case = case.copy()
        self.userAction.append(self.case)

    def push(self, case):
        self.userAction.append(case.copy())

    def pop(self):
        self.userAction.pop()
        if len(self.userAction) == 0:
            self.userAction.append(self.case)
