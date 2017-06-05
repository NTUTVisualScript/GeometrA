from tkinter import ttk
from cv2img import CV2Img
from adb_roboot import ADBRobot
import xml.etree.cElementTree as ET
from PIL import Image
from finder.template_finder import TemplateFinder
from finder.template_matcher import TemplateMatcher
from MessageUI import Message
from LoadFile import LoadFile
import time
import os

ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(ROOT_DIR, "screenshot_pic")

sorce_image = None

def IMG_PATH(name):
    return os.path.join(RESOURCES_DIR, name)

def template_finder(target_image):
    robot = ADBRobot()
    source = CV2Img()
    source.load_file(IMG_PATH(robot.screenshot()), 0)
    target = CV2Img()
    target.load_PILimage(target_image)
    finder = TemplateFinder(source)
    results = finder.find_all(target, 0.9)
    print(len(results))
    for i in range(len(results)):
        print(results[i].x,"  ", results[i].y,"  ", results[i].w,"  ", results[i].h,"\n")

    if len(results) < 1:
        return "faile"
    elif len(results) == 1:
        coordinate_x, coordinate_y = source.coordinate(results[0])
        robot.tap(coordinate_x, coordinate_y)
        return "success"
    elif len(results) > 1:
        return "too more"


def assert_finder(target_image):
    robot = ADBRobot()
    source = CV2Img()
    source.load_file(IMG_PATH(robot.screenshot()), 0)
    target = CV2Img()
    target.load_PILimage(target_image)
    finder = TemplateFinder(source)
    results = finder.find_all(target, 0.9)
    print(len(results))

    if len(results) < 1:
        return False
    elif len(results) == 1:
        return True
    elif len(results) > 1:
        return True
    # robot = ADBRobot()
    # source = CV2Img()
    # source.load_file(IMG_PATH(robot.screenshot()), 0)
    # target = CV2Img()
    # target.load_PILimage(target_image)
    # ratio = min(target.rows / 12, target.cols / 12)
    # matcher = TemplateMatcher(source, target, 1, ratio)
    # result = matcher.next()
    # print(result)
    # result_image = source.crop(result)
    # if result_image == target:
    #     return True
    # else:
    #     return False

class TestAdepter():
    def Single_Test(self, actioncombobox , value, valueImage , node_path):
        self.robot = ADBRobot()
        self.action = []
        self.value = []
        self.image = []
        self.path_list = []

        self.action.append(actioncombobox.get())
        if valueImage != None:
            self.value.append(None)
        else:
            self.value.append(value.get())

        self.image.append(valueImage)
        self.path_list.append(node_path)

        return self.Action()

    def Open_Single_Test(self, actioncombobox , value, valueImage , node_path):
        self.robot = ADBRobot()
        self.action = []
        self.value = []
        self.image = []
        self.path_list = []

        self.action.append(actioncombobox)
        if valueImage != None:
            self.value.append(None)
        else:
            self.value.append(value)

        self.image.append(valueImage)
        self.path_list.append(node_path)

        return self.Action()

    # def All_Test(self, actioncomboboxlist, valuelist, valueImagelist , node_path_list):
    #     self.robot = ADBRobot()
    #     self.action = []
    #     self.value = []
    #     self.image = []
    #     self.path_list = []
    #
    #     print(len(actioncomboboxlist))
    #     for i in range(len(actioncomboboxlist)):
    #         self.action.append(actioncomboboxlist[i].get())
    #         if valueImagelist[i] != None:
    #             self.value.append(None)
    #         else:
    #             self.value.append(valuelist[i].get())
    #
    #         if i < len(valueImagelist):
    #             self.image.append(valueImagelist[i])
    #             self.path_list.append(node_path_list[i])
    #     return self.Action()

    def Action(self):
        self.message = Message.getMessage(self)
        index = 0
        self.ActionStatus = "Success"
        for i in self.action:
            if self.ActionStatus == "Success":
                time.sleep(1)
                if str(i) == "":
                    break
                if str(i) == "Click":
                    #print(index)
                    self.ActionStatus = self.ClickImage(index)
                elif str(i) == "Drag":
                    #print(self.action.index(i))
                    self.ActionStatus = self.DragValue(index)
                elif str(i) == "Input":
                    #print(self.action.index(i))
                    self.ActionStatus = self.InputValue(index)
                elif str(i) == "TestCase":
                    #print(self.action.index(i))
                    self.ActionStatus = self.TestCasePath(index)
                elif str(i) == "Android Keycode":
                    #print(self.action.index(i))
                    self.ActionStatus = self.Send_Key_Value(index)
                elif str(i) == "Assert Exist":
                    #print(self.action.index(i))
                    self.ActionStatus = self.ExistsImage(index)
                elif str(i) == "Assert Not Exist":
                    #print(self.action.index(i))
                    self.ActionStatus = self.ExistsImage(index)
                    if self.ActionStatus == "Success":
                        self.ActionStatus = "Error"
                    else:
                        self.ActionStatus = "Success"

                index = index+1

        return self.ActionStatus

    def ExistsValue(self, index):
        self.treeview = ttk.Treeview()
        self.XMLFile = ET.ElementTree(file=self.robot.get_uiautomator_dump())
        self.tree_info("", self.XMLFile)
        self.path_range = len(self.path_list[index])
        self.node_item = None
        self.Find_image_Path(index, 1, "")

        if self.node_item != None:
            return "Success"
        else:
            return "Error"

    def ClickValue(self,index):
        self.treeview = ttk.Treeview()
        self.XMLFile = ET.ElementTree(file=self.robot.get_uiautomator_dump())
        self.tree_info("", self.XMLFile)
        self.path_range =len(self.path_list[index])
        self.node_item = None
        self.Find_image_Path(index, 1, "")

        if self.node_item != None:
            left, top, right, bottom = self.bounds_split(self.treeview.item(self.node_item)["values"][1])
            self.robot.tap((right+left)/2, (bottom+top)/2)
            return "Success"
        else:
            return "Error"

    def ExistsImage(self, index):
        status = assert_finder(self.image[index])
        if status == True:
            print("Success : Find This Image and Node")
            self.message.InsertText("Success : Find This Image and Node")
            return "Success"
        else:
            print("Error : Not Find Image and Node")
            self.message.InsertText("Error : Not Find Image and Node")
            return "Error"

    def ClickImage(self, index):
        status = template_finder(self.image[index])
        if status =="success":
            self.message.InsertText("Success : Click Image\n")
            return "Success"
        elif status == "too more":
            return self.ClickValue(index)
        else:
            print("Error : Not Find Image")
            self.message.InsertText("Error : Not Find Image\n")
            return "Error"

    def tree_info(self,id , treeinfo):
        for elem in treeinfo.findall('node'):
            if elem is None: return
            id_child = self.treeview.insert(id, "end", elem , text="(" + str(elem.get('index')) + ") "
                                                                   + str(elem.get('class')) + "  "
                                                                   ,  values=( str(elem.get('text')),str(elem.get('bounds'))) , open=True)
            self.tree_info(id_child, elem)

    def Find_image_Path(self, index, depth, item):
        if depth < self.path_range:
            children_node = self.treeview.get_children(item)
            for child in children_node:
                if self.node_item == None:
                    if self.path_list[index][depth-1][0] == self.treeview.item(child)["text"] :
                        print("find ", self.path_list[index][depth - 1][0],",  treeview node :", self.treeview.item(child)["text"])
                        depth = depth + 1
                        self.Find_image_Path(index, depth,child)
                    else :
                        print("not find ", self.path_list[index][depth-1][0],",  treeview node :", self.treeview.item(child)["text"])

        if depth == self.path_range:
            children_node = self.treeview.get_children(item)
            for child in children_node:
                if self.node_item == None:
                    if self.path_list[index][depth-1][0] == self.treeview.item(child)["text"] :
                        text = self.treeview.item(child)["values"][0]
                        if str(text) == self.path_list[index][depth-1][1]:
                            self.node_item = child
                            print("Find Node ", self.path_list[index][depth - 1][0])
                        else:
                            print("Text not same between ", str(text), self.path_list[index][depth - 1][0])
                    else:
                        print("Not Find ", self.path_list[index][depth - 1][0])

    def bounds_split(self,obj_bounds):
        bounds = obj_bounds.split('[')
        right_bounds = bounds[1].split(']')
        left_bounds = bounds[2].split(']')

        right_top = right_bounds[0].split(',')
        left_bottom = left_bounds[0].split(',')

        left = int(right_top[0])
        top = int(right_top[1])
        right = int(left_bottom[0])
        bottom = int(left_bottom[1])
        print(left, top, right, bottom)

        return left, top, right, bottom

    def DragValue(self, index):
        coordinatevalue = str(self.value[index])
        try:
            coordinate = coordinatevalue.split(",")
            print(coordinate)
            X_coordinate_start = coordinate[0].split('=')
            X_start = X_coordinate_start[1]
            print(X_start)
            Y_coordinate_start = coordinate[1].split('=')
            Y_start = Y_coordinate_start[1]
            print(Y_start)

            X_coordinate_end = coordinate[2].split('=')
            X_end = X_coordinate_end[1]
            Y_coordinate_end = coordinate[3].split('=')
            Y_end = Y_coordinate_end[1]

        except:
            print("Coordinate Value split Error : ", coordinatevalue)
            return "Error"

        try:
            self.robot.drag_and_drop(int(X_start), int(Y_start), int(X_end), int(Y_end))
            print("Drag Coordinate is start x = ", int(X_start), " y = ", int(Y_start), "to  x = ", int(X_end), " y = ",
                  int(Y_end))
            return "Success"
        except:
            print("Drag and drop Error")
            return "Error"


    def InputValue(self, index):
        print(self.value[index])
        return self.robot.input_text(self.value[index])

    def TestCasePath(self, index):
        testcase_load = LoadFile()
        testcase_load.Decoder_Json(self.value[index])
        actioncombo_list, value_list, valueImage_list, nodepath_list = testcase_load.get_Loading_Data()
        run_testcase = TestAdepter()
        self.start = None
        self.end = None
        self.forloop = None
        for i in range(len(actioncombo_list)):
            if actioncombo_list[i] != "":
                if actioncombo_list[i] == "Loop":
                    if value_list[i] =="":
                        return "Error"
                    else:
                        self.start = i + 1
                        self.forloop = int(value_list[i]) - 1
                if actioncombo_list[i] == "Stop":
                    print(actioncombo_list[i])
                    self.end = i
                    self.ForLoop(actioncombo_list, value_list, valueImage_list, nodepath_list)
                if actioncombo_list[i] == "Sleep(s)":
                    time.sleep(int(value_list[i]))
                else:
                    status = run_testcase.Open_Single_Test(actioncombo_list[i], value_list[i], valueImage_list[i], nodepath_list[i])
                    if status == "Error":
                        break
                if i == len(actioncombo_list) - 1 and self.end == None and self.start != None:
                    status == "Error"
                    break
        return status

    def ForLoop(self,actioncombo_list, value_list, valueImage_list, nodepath_list):
        if self.CheckLoop():
            run_testcase = TestAdepter()
            for i in range(self.forloop):
                index = self.start
                while index < self.end:
                    if actioncombo_list[index] != "":
                        status = run_testcase.Open_Single_Test(actioncombo_list[index], value_list[index], valueImage_list[index],
                                                          nodepath_list[index])
                        index = index + 1
                        if status == "Error":
                            break
        else:
            status =  "Error"

        self.forloop = None
        self.start = None
        self.end = None
        return status

    def CheckLoop(self):
        if self.forloop!=None and self.start!=None and self.end != None:
            return True
        else:
            return False


    def Send_Key_Value(self, index):
        try:
            self.robot.send_key(self.value[index])
            return "Success"
        except:
            print("Input Value Error")
            self.message.InsertText("The Android Keycade Error\n")
            return "Error"



