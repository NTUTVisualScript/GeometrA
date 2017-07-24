class Record:
    def __init__(self):
        self.redo = []
        self.undo = []

    def action(self, testCase):
        self.redo.append(testCase)
        self.undo.clear

    def redo(self):
        
