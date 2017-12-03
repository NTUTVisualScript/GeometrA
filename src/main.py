from Ctrl.WorkSpace import WorkSpace
from Ctrl.ToolBar.ToolBar import ToolBar
class View:
    def __init__(self):
        self.workspace = WorkSpace()
        self.tools = ToolBar()


if __name__ == '__main__':
    view = View()
