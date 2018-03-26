import os, shutil
import json

from xml.etree import ElementTree as ET

from VisualScript.src.File.Project import Project

class WorkSpace:
    def __init__(self, path=None, project=None):
        self.projects = {}
        if path and project:
            self.load(path, project)
        self.focus = {
            "Project":"",
            "Suite":"",
            "Case":"",
        }


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

    def delete(self, name):
        if not name in self.projects:
            raise Exception('Project: "' + name +'" not exist')
        shutil.rmtree(self.projects[name].path)
        del self.projects[name]

    def rename(self, origin, new):
        projectPath = self.projects[origin].path
        newProjectPath = projectPath[0:projectPath.rindex('/')] + '/' + new
        os.remove(projectPath + '/' + origin + '.json')
        os.rename(projectPath, newProjectPath)
        self.projects[new] = self.projects.pop(origin)
        self.projects[new].path = newProjectPath
        for suite in self.projects[new].suites:
            self.projects[new].suites[suite].path = newProjectPath + '/' + suite
        self.projects[new].updateRecord()

    def getJSON(self, p):
        if not p in self.projects:
            raise Exception('Project: "' + p +'" not exist')
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

    def setFocus(self, focus):
        self.focus = focus

    def getFocusPath(self):
        project = self.projects[self.focus['Project']]
        suite = project.suites[self.focus['Suite']]
        path = suite.path + '/' + self.focus['Case'] + '/testcase.xml'
        return path

    def save(self, data):
        path = self.getFocusPath();
        with open(path, 'w') as f:
            f.write(data)
