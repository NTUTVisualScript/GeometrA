import os
import time
import xml.etree.cElementTree as ET
from tkinter import ttk

from LoadFile import LoadFile
from MessageUI import Message
from TestCaseData import TestCaseData
from adbRobot import ADBRobot
from cv2img import CV2Img
from finder.template_finder import TemplateFinder
from HTML.step import HtmlTestStep


ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(ROOT_DIR, "screenshot_pic")

sorce_image = None

def IMG_PATH(name):
    return os.path.join(RESOURCES_DIR, name)

def Drag_image(source_image, x1,y1,x2,y2):
    source = CV2Img()
    source.load_file(source_image, 1)
    source.draw_Arrow(x1,y1,x2,y2)
    source.save(source_image)

def Click_image(source_image, x1,y1):
    source = CV2Img()
    source.load_file(source_image, 1)
    source.draw_circle( x1, y1)
    source.save(source_image)

def Exist_image(source_image, x1,y1,x2,y2):
    drawcircle = CV2Img()
    drawcircle.load_file(source_image, 1)
    drawcircle.draw_rectangle(x1,y1,x2,y2)
    drawcircle.save(source_image)

def template_finder(source_image, target_image):
    robot = ADBRobot()
    source = CV2Img()
    source.load_file(source_image, 0)
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
        drawcircle = CV2Img()
        drawcircle.load_file(source_image, 1)
        drawcircle.draw_circle(int(coordinate_x), int(coordinate_y))
        drawcircle.save(source_image)
        robot.tap(coordinate_x, coordinate_y)
        return "success"
    elif len(results) > 1:
        return "too more"


def assert_finder(source_image, target_image):
    robot = ADBRobot()
    source = CV2Img()
    source.load_file(source_image, 0)
    target = CV2Img()
    target.load_PILimage(target_image)
    finder = TemplateFinder(source)
    results = finder.find_all(target, 0.9)
    print(len(results))

    if len(results) < 1:
        return "faile"
    elif len(results) == 1:
        drawcircle = CV2Img()
        drawcircle.load_file(source_image, 1)
        drawcircle.draw_result_range(results[0])
        drawcircle.save(source_image)
        return "success"
    elif len(results) > 1:
        return "too more"
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
        self.htmlstep = HtmlTestStep.getHtmlTestStep()
        self.step_before_image = ""
        self.step_after_image = ""

    def Run(self, actioncombobox , value, valueImage , node_path):

        self.action, self.value, self.image, self.node_path = actioncombobox , value, valueImage , node_path

        return self.Action()

    def get_action_before_Screen(self):
        filePath = self.robot.before_screenshot()
        self.step_before_image = filePath

    def get_action_after_Screen(self):
        filePath = self.robot.after_screenshot()
        self.step_after_image = filePath

    def run_single(self, line, action, value, image, node_path):
        self.get_action_before_Screen()

        status = self.Run( action, value, image, node_path)
        self.htmlstep.step_before(self.step_before_image)
        self.ScreenShot_update()
        self.get_action_after_Screen()
        self.htmlstep.step_after(self.step_after_image)
        self.run_status(line, status, self.testcaseName)
        #self.get_action_after_Screen()

        return status

    def ScreenShot_update(self):
        self.update.set_run_test_screenshot(self.step_before_image)

    def run_all(self, start = None, end = None):
        from GUI.ScreenShotUI import ScreenshotUI
        self.update = ScreenshotUI.getScreenShotUI(self)
        self.count = 0
        status = ""
        if end is None:
            end = len(self.actionlist)
        if start is None:
            start = 0
        for n in range(start, end, +1):
            if self.actionlist[n] != "":
                self.count+=1
                if self.actionlist[n] == "Loop Begin":
                    status ,loopcount= self.run_loop(n)
                    self.count = self.count + loopcount
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
                    self.htmlstep.set_step(self.testcaseName, n, action, status, value, image)

                    if status == "Error":
                        break
        self.update.remove_run_test_screenshot()

        return status, self.count


    def run_loop(self, start):
        print(self.loop_begin)
        print(self.loop_end)
        index = self.loop_begin.index(start)
        end = self.loop_end[index]

        for i in range(int(self.valuelist[start]) - 1):
            status, count = self.run_all(start+1, end)
        return status, count

    def Action(self):

        index = 0
        self.ActionStatus = "Success"
        for i in self.action:
            if self.ActionStatus == "Success":
                if str(i) == "":
                    break
                if str(i) == "Click":
                    self.ActionStatus = self.ClickImage(index)
                    time.sleep(1)
                elif str(i) == "Drag":
                    #print(self.action.index(i))
                    self.ActionStatus = self.DragValue(index)
                    time.sleep(1)
                elif str(i) == "Set Text":
                    #print(self.action.index(i))
                    self.ActionStatus = self.InputValue(index)
                elif str(i) == "TestCase":
                    #print(self.action.index(i))
                    self.ActionStatus, count = self.TestCasePath(index)
                    self.count = self.count + count
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
            Click_image(self.step_before_image, (right+left)/2, (bottom+top)/2)
            return "Success"
        else:
            return "Error"

    def ExistsValue(self,index):
        self.treeview = ttk.Treeview()
        self.XMLFile = ET.ElementTree(file=self.robot.get_uiautomator_dump())
        self.tree_info("", self.XMLFile)
        self.path_range =len(self.node_path[index])
        self.node_item = None
        self.Find_image_Path(index, 1, "")

        if self.node_item != None:
            left, top, right, bottom = self.bounds_split(self.treeview.item(self.node_item)["values"][1])
            Exist_image(self.step_before_image, left, top, right, bottom)
            return "Success"
        else:
            return "Error"

    def ExistsImage(self, index):
        status = assert_finder(self.step_before_image, self.image[index])
        if status == "success":
            print("Success : Find This Image and Node")
            #self.message.InsertText("Success : Find This Image and Node")
            return "Success"
        elif status == "too more":
            return self.ExistsValue(index)
        else:
            print("Error : Image and Node Not Find")
            self.message.InsertText("Error : Image and Node Not Find")
            return "Error"

    def ClickImage(self, index):
        status = template_finder(self.step_before_image, self.image[index])

        if status =="success":
            #self.message.InsertText("Success : Click Image\n")
            return "Success"
        elif status == "too more":
            return self.ClickValue(index)
        else:
            print("Error : Image Not Find")
            self.message.InsertText("Error : Image Not Find\n")
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
            Drag_image(self.step_before_image, int(X_start), int(Y_start), int(X_end), int(Y_end))
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
            status, count = testcase.run_all()
        else:
            testcase.message.InsertText("The Test case have some problem, please check Test Case File : \n"+ self.value[index] +" !\n")

        return status, count

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
