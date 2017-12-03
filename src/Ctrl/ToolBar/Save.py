from browser import document

class Save:
    def __init__(self):
        document['Save'].bind('click', self.saveProject)
