import os

from File.Project import Project

class WorkSpace:
    def __init__(self, path, project):
        self.projects = {}
        self.add(path, project)

    def add(self, path, project):
        name = project[0]

        # if not os.path.isdir(path + "/" + name):
        #     print(path + '/' + name)
        #     print(os.path.isdir(path + '/' + name))
        #     raise Exception('Project: "' + name + '" is not in the path')

        projectPath = path + '/' + name
        self.projects[name] = Project(projectPath, project[1][name])

    def getJSON(self, p):
        if not p in self.projects:
            raise Exception('Project: "' + name +'" not exist')
        d = self.projects[p].getJSON()
        result = {p:d}
        return result

    def getTreeJSON(self):
        result = []
        for p in self.projects:
            d = {}
            d["text"] = p
            d["children"] = self.projects[p].getTreeJSON()
            result.append(d)
        return result
