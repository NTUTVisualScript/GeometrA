from browser import window, alert
from File.WorkSpace import WorkSpace as wsModel
import os

class WorkSpace:
    def __init__(self):
        self.UI = window.FileTree.new()
        self.space = wsModel(path, p)
        json = self.space.getTreeJSON()
        self.UI.update(json)
