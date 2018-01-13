import os
import json

class Creator:
    def new(self, info):
        # Decode information
        path = info['path']
        self.projectPath = path + info['project']
        if os.path.isdir(self.projectPath):
            raise Exception('The directory is exist!')
        suitePath = self.projectPath + '/' + info['suite']
        casePath = suitePath + '/' + info['case']

        # Make the directories and the files
        os.mkdir(self.projectPath)
        os.mkdir(suitePath)
        os.mkdir(casePath)
        with open(casePath + '/testcase.json', 'w') as f:
            f.write(json.dumps({}))

        self.writeJSON(info)

    def writeJSON(self, info):
        # Get the path of record file
        jsonPath = self.projectPath + '/' + info['project'] + '.json'

        # Encode a json object
        log = json.dumps([info['project'], {
            info['project']: {
                info['suite']: [info['case'], ],
            },
        }])

        # Out put the file.
        with open(jsonPath, 'w') as f:
            f.write(log)
