from browser import window, alert
from File.WorkSpace import WorkSpace as wsModel
import os

class WorkSpace:
    def __init__(self):
        self.UI = window.FileTree.new()
        path = 'D:'
        p = ['Project', {'Project':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        self.space = wsModel(path, p)
        json = self.space.getTreeJSON()
        self.UI.update(json)
        # self.UI.right = self.selected

    def selected(self, e, d):
        print("The selected node is: ")
        print(d)
