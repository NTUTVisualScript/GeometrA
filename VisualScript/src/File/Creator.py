import os

class Creator:
    def new(self, info):
        if os.path.exists(info['project']):
            return
