import os
import json

from GeometrA.src import WORKSPACE

def new(info):
    # Decode information
    path = info['path']
    projectPath = path + '/' + info['project']
    if os.path.isdir(projectPath):
        raise Exception('The directory is exist!')
    project = info['project']
    suite = info['suite']
    case = info['case']

    WORKSPACE.add(path, project)
    WORKSPACE.projects[project].add(suite)
    WORKSPACE.projects[project].add(suite, case)

def load(path, workspace=None):
    # ws as a component for unittest
    if not workspace:
        workspace = WORKSPACE

    with open(path, 'r') as f:
        data = json.load(f)
    try:
        projectPath = path[:path.rindex('/', 0, path.rindex('/'))]
        workspace.load(projectPath, data)
    except Exception as e:
        raise e
