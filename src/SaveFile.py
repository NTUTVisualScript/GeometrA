import json
import os
import tkinter.filedialog

class SaveFile():
    def SaveTestCase(self, actioncomboboxlist , valuelist, valueImagelist , node_path_list):
        dirpath = tkinter.filedialog.askdirectory()

        if dirpath is None: return

        print(dir)
        self.action = []
        self.value = []
        self.image = []
        self.path_list = []

        print(len(actioncomboboxlist))
        for i in range(len(actioncomboboxlist)):
            if actioncomboboxlist[i].get() != "":
                self.action.append(actioncomboboxlist[i].get())
                if valueImagelist[i] != None:
                    self.value.append(None)
                else:
                    self.value.append(valuelist[i].get())

                if i < len(valueImagelist):
                    self.image.append(valueImagelist[i])
                    self.path_list.append(node_path_list[i])


        dataArray = {}

        for i in range(len(self.action)):
            data = {}
            data["action"] = self.action[i]
            data["value"] = self.value[i]
            if self.image[i] != None:
                if not os.path.isdir(dirpath + "/image"):
                    os.makedirs(dirpath + "/image")
                imagepath = "/image/"+ str(self.action[i]) + "_" + str(i) + ".jpg"
                img = self.image[i]
                if os.path.isfile(imagepath):
                    os.remove(imagepath)

                try:
                    img.save(dirpath + imagepath, "JPEG")
                except AttributeError:
                    print("Couldn't save image {}".format(img))

                print(imagepath)
                data["image"] = imagepath
                print(self.path_list[i])
                data["image_node_path"] = {}
                for j in range(len(self.path_list[i])):
                    data["image_node_path"][str(j+1)] = self.path_list[i][j]
            else:
                data["image"] = None
                data["image_node_path"] = None

            dataArray[i+1] = data
        print(dataArray)
        with open(dirpath +'/testcase.json', 'w', encoding='utf-8') as fp:
            json.dump(dataArray, fp, indent=2)

        json_str = json.dumps(dataArray)
        print(json_str)

        return dirpath