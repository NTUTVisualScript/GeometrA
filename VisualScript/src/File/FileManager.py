import os
import json

from VisualScript.src.main import WORKSPACE
from VisualScript.src.File.WorkSpace import WorkSpace

def new(info):
    # Decode information
    path = info['path']
    projectPath = path + info['project']
    if os.path.isdir(projectPath):
        raise Exception('The directory is exist!')
    suitePath = projectPath + '/' + info['suite']
    casePath = suitePath + '/' + info['case']

    # Make the directories and the files
    os.mkdir(projectPath)
    os.mkdir(suitePath)
    os.mkdir(casePath)
    with open(casePath + '/testcase.json', 'w') as f:
        f.write(json.dumps({}))

    writeJSON(info, projectPath)

def writeJSON(info, path):
    # Get the path of record file
    jsonPath = path + '/' + info['project'] + '.json'

    # Encode a json object
    log = json.dumps([info['project'], {
        info['project']: {
            info['suite']: [info['case'], ],
        },
    }])

    # Out put the file.
    with open(jsonPath, 'w') as f:
        f.write(log)

def load(path, workspace=None):
    # ws as a component for unittest
    if not workspace:
        workspace = WORKSPACE

    with open(path, 'r') as f:
        data = json.load(f)

    projectPath = path[:path.rindex('/', 0, path.rindex('/'))]
    workspace.add(projectPath, data)
    return True
