from browser import window
from File.WorkSpace import WorkSpace as wsModel

class WorkSpace:
    def __init__(self):
        self.UI = window.FileTree.new()
        self.space = wsModel()
        self.UI.update(self.space.getTreeJSON())
