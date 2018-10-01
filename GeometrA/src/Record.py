from GeometrA.src import WORKSPACE
from GeometrA.src.File.FileManager import load

import json
import os

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
        try:
            load(p, workspace = workspace)
        except Exception as e:
            os.remove(RECORD_FILE) #TODO: need to fix
            raise e
