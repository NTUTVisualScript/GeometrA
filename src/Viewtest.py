from tkinter import ttk
from cv2img import CV2Img
from adb_roboot import ADBRobot
import xml.etree.cElementTree as ET
from finder.template_finder import TemplateFinder
from TestCaseData import TestCaseData
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

class TestAdepter(TestCaseData):
    def __init__(self):
        self.robot = ADBRobot()
        self.action = []
        self.value = []
        self.image = []
        self.node_path = []
        self.actionlist = []
        self.valuelist = []
        self.imagelist = []
        self.node_path_list = []
        self.loop_begin = []
        self.loop_end = []
        self.testcaseName = ""
        self.message = Message.getMessage(self)

    def Run(self, actioncombobox , value, valueImage , node_path):

        self.action, self.value, self.image, self.node_path = actioncombobox , value, valueImage , node_path

        return self.Action()

    def run_single(self, line, action, value, image, node_path):
        status = self.Run( action, value, image, node_path)
        self.run_status(line, status, self.testcaseName)

        return status

    def run_all(self, start = None, end = None):
        if end is None:
            end = len(self.actionlist)
        if start is None:
            start = 0
        for n in range(start, end, +1):
            if self.actionlist[n] != "":
                if self.actionlist[n] == "Loop Begin":
                    self.run_loop(n)
                else:
                    action = []
                    value = []
                    image = []
                    node_path = []
                    action.append(self.actionlist[n])
                    value.append(self.valuelist[n])
                    image.append(self.imagelist[n])
                    node_path.append(self.node_path_list[n])
                    status = self.run_single( n, action, value, image, node_path)
                    if status == "Error":
                        break


    def run_loop(self, start):
        print(self.loop_begin)
        print(self.loop_end)
        index = self.loop_begin.index(start)
        end = self.loop_end[index]

        for i in range(int(self.valuelist[start]) - 1):
            self.run_all(start+1, end)

    def Action(self):

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
                elif str(i) == "Sleep(s)":
                    #print(self.action.index(i))
                    self.ActionStatus = self.Sleep(index)
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
        self.path_range = len(self.node_path[index])
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
        self.path_range =len(self.node_path[index])
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
            #self.message.InsertText("Success : Find This Image and Node")
            return "Success"
        else:
            print("Error : Not Find Image and Node")
            self.message.InsertText("Error : Not Find Image and Node")
            return "Error"

    def ClickImage(self, index):
        status = template_finder(self.image[index])

        if status =="success":
            #self.message.InsertText("Success : Click Image\n")
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
                    if self.node_path[index][depth-1][0] == self.treeview.item(child)["text"] :
                        print("find ", self.node_path[index][depth - 1][0],",  treeview node :", self.treeview.item(child)["text"])
                        depth = depth + 1
                        self.Find_image_Path(index, depth,child)
                    else :
                        print("not find ", self.node_path[index][depth-1][0],",  treeview node :", self.treeview.item(child)["text"])

        if depth == self.path_range:
            children_node = self.treeview.get_children(item)
            for child in children_node:
                if self.node_item == None:
                    if self.node_path[index][depth-1][0] == self.treeview.item(child)["text"] :
                        text = self.treeview.item(child)["values"][0]
                        if str(text) == self.node_path[index][depth-1][1]:
                            self.node_item = child
                            print("Find Node ", self.node_path[index][depth - 1][0])
                        else:
                            print("Text not same between ", str(text), self.node_path[index][depth - 1][0])
                    else:
                        print("Not Find ", self.node_path[index][depth - 1][0])

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

        name = self.value[index].split('/')
        foldername = str(name.pop())

        testcase = TestAdepter()
        actioncombo_list, value_list, valueImage_list, node_path_list = testcase_load.get_Loading_Data()
        testcase_status = testcase.load_file_set_data(actioncombo_list, value_list, valueImage_list, node_path_list)

        testcase.testcaseName = foldername + " : "

        if testcase_status:
            testcase.run_all()
        else:
            testcase.message.InsertText("The Test case have some problem, please check Test Case File : \n"+ self.value[index] +" !\n")

    def Sleep(self, index):
        try:
            time.sleep(int(self.value[index]))
            return "Success"
        except:
            return "Error"

    def Send_Key_Value(self, index):
        try:
            self.robot.send_key(self.value[index])
            return "Success"
        except:
            print("Input Value Error")
            self.message.InsertText("The Android Keycade Error\n")
            return "Error"
