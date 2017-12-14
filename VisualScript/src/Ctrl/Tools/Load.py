from browser import document
class Load:
    def __init__(self):
        document['Load'].bind('click', self.loadProject)

    def loadProject(self, env):
        
