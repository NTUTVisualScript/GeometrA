from VisualScript.src import WORKSPACE
from VisualScript.src.File.FileManager import load

import json

RECORD_FILE = './record.log'

def exportLog(workspace = None):
    if not workspace:
        workspace = WORKSPACE
    log = {
        'WorkSpace': workspace.log()
    }

    info = str(log).replace("'", '"')
    with open(RECORD_FILE, 'w') as f:
        f.write(info)

def loadLog(workspace = None):
    if not workspace:
        workspace = WORKSPACE

    with open(RECORD_FILE, 'r') as f:
        result = f.read()

    log = json.loads(result)
    for p in log['WorkSpace']:
        load(p, workspace = workspace)
