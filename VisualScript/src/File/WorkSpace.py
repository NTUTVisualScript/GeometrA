import os
import json

from VisualScript.src.File.Project import Project

class WorkSpace:
    def __init__(self, path=None, project=None):
        self.projects = {}
        if path and project:
            self.load(path, project)

    def load(self, path, project):
        name = project[0]

        if not os.path.isdir(path + "/" + name):
            raise Exception('Project: "' + name + '" is not in the path')

        projectPath = path + '/' + name
        self.projects[name] = Project(projectPath, project[1][name])

    def add(self, path, name):
        if os.path.isdir(path + '/' + name):
            raise Exception('Project: "' + name + '" is already exists!')
        projectPath = path + '/' + name
        os.mkdir(projectPath)
        with open (projectPath + '/' + name + '.json', 'w') as f:
            data = [name, {name:{}}]
            f.write(json.dumps(data))
        with open (projectPath + '/' + name + '.json', 'r') as f:
            data = json.load(f)
        self.load(path, data)

    def getJSON(self, p):
        if not p in self.projects:
            raise Exception('Project: "' + name +'" not exist')
        d = self.projects[p].getJSON()
        result = [p, {p:d}]
        return result

    def getTreeJSON(self):
        result = []
        for p in self.projects:
            d = {}
            d["text"] = p
            d["children"] = self.projects[p].getTreeJSON()
            result.append(d)
        return result

    def log(self):
        pathList = []
        for p in self.projects:
            pathList.append(self.projects[p].path + '/' + p + '.json')
        return pathList
