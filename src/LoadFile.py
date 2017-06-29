import json
import os
import tkinter.filedialog
from PIL import Image

class LoadFile():
    def __init__(self):
        self.folderpath = ""
        self.foldername = ""

    def LoadTestCasePath(self):

        dirpath = tkinter.filedialog.askdirectory()
        print(dirpath)
        if dirpath is None or dirpath == "": return

        self.folderpath = dirpath

        name = dirpath.split('/')
        self.foldername = str(name.pop())


        return dirpath

    def get_folderName(self):
        print(self.foldername)
        return self.foldername


    def Decoder_Json(self, dirpath):
        with open(dirpath +'/testcase.json', 'r') as f:
            dataArray = json.load(f)

        print(dataArray)

        print(len(dataArray))

        self.action_list = []
        self.value_list = []
        self.image_list = []
        self.path_list = []

        for i in range(len(dataArray)):
            value = dataArray[str(i+1)]
            print(value)
            self.action_list.append(value['action'])
            self.value_list.append(value['value'])

            if value['image'] !=None:
                photo = Image.open(dirpath + str(value['image']))
                self.image_list.append(photo)
            else:
                self.image_list.append(None)

            if value['image_node_path'] != None:
                node_path = value['image_node_path']
                print(len(node_path))
                node_list = []
                for j in range(len(node_path)):
                    node = node_path[str(j+1)]
                    print(node)
                    node_list.append(node)

                self.path_list.append(node_list)
            else:
                self.path_list.append(None)


    def get_Loading_Data(self):
        return self.action_list, self.value_list, self.image_list, self.path_list