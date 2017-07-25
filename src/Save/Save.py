import json
import os
import tkinter.filedialog

class Save():
    def saveTestCase(self, case):
        dirPath = tkinter.filedialog.askdirectory()
        if dirPath is None: return
        self.action = []
        self.value = []

        for i in range(case.getSize()):
            self.action.append(case.getSteps(i).getAction())
            self.value.append(case.getSteps(i).getValue())


        dataDic = {}

        for i in range(len(self.action)):
            data = {}
            data['action'] = self.action[i]
            data['value'] = self.value[i]
            if '.png' in self.value[i]:
                if not os.path.isdir(dirPath + '/image')
                    os.makedirs(dirPath + '/image')
                imagePath = '/image/' + str(self.action[i]) + '_' + str(i) + '.png'

                if os.path.isfile(imagePath):
                    os.remove(imagePath)

                '''
                decide how to save image int the test case
                '''
                # try:
                #     img.save(dirPath + imagePath, 'PNG')
                # except AttributeError:
                #     print("Couldn't save imgae {}".format(img))

            dataDic[i+1] = data

        with open(dirPath + '/TestCase.json', 'w', encoding = 'utf-8') as fp:
            json.dump(dataArray, fp, indent = 2)
