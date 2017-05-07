import subprocess
from tkinter import ttk
import cv2
from cv2img import CV2Img
from adb_roboot import ADBRobot
import xml.etree.cElementTree as ET
from PIL import Image, ImageTk
from rectangle import Rectangle
from finder.template_finder import TemplateFinder
from finder.template_matcher import TemplateMatcher
from uiautomator import device as d
import unittest
import time
import os

ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(ROOT_DIR, "screenshot_pic")

sorce_image = None

def IMG_PATH(name):
    return os.path.join(RESOURCES_DIR, name)

def template_finder(target_image,left, top, right, bottom):
    robot = ADBRobot()
    source = CV2Img()
    source.load_file(IMG_PATH(robot.screenshot()), 1)
    # cropimg = source.crop(Rectangle(left, top, right - left, bottom - top))
    # cropimg.show()
    # source = cropimg
    #source.load_PILimage(source_image)
    #source.show()
    target = CV2Img()
    target.load_PILimage(target_image)
    #target.show()
    finder = TemplateFinder(source)
    results = finder.find_all(target, 0.9)
    print(results)
    if results != []:
        return "success"
    else:
        return "faile"
    #return "success"
    # coordinate_x, coordinate_y = source.coordinate(results[0])
    # robot.tap(coordinate_x, coordinate_y)


def assert_finder(target_image,left, top, right, bottom):
    robot = ADBRobot()
    source = CV2Img()
    source.load_file(IMG_PATH(robot.screenshot()), 1)
    # source.show()
    # cropimg = source.crop(Rectangle(left, top, right - left, bottom - top))
    # cropimg.show()
    # source = cropimg
    target = CV2Img()
    target.load_PILimage(target_image)
    #target.show()
    ratio = min(target.rows / 12, target.cols / 12)
    matcher = TemplateMatcher(source, target, 1, ratio)
    result = matcher.next()
    result_image = source.crop(result)
    if result_image == target:
        return True
    else:
        return False

class TestAdepter(unittest.TestCase):
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

        self.Action()

    # def Test(self, actioncomboboxlist, valuelist, valueImagelist , node_path_list):
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
    #
    #     self.Action()

    def Action(self):
        subprocess.check_output('adb kill-server')
        subprocess.check_output('adb devices')
        index = 0
        self.ActionError = False
        for i in self.action:
            if self.ActionError == False:
                time.sleep(1)
                if str(i) == "":
                    break
                if str(i) == "Click":
                    #print(index)
                    self.ClickValue(index)
                elif str(i) == "Drag":
                    #print(self.action.index(i))
                    self.DragValue(index)
                elif str(i) == "Input":
                    #print(self.action.index(i))
                    self.InputValue(index)
                elif str(i) == "Send Key":
                    #print(self.action.index(i))
                    self.Send_Key_Value(index)
                elif str(i) == "Exists":
                    #print(self.action.index(i))
                    self.ExistsValue(index)
                index = index+1

    def ExistsValue(self, index):
        filePath = IMG_PATH(self.robot.screenshot())
        self.photo = Image.open(filePath)
        self.treeview = ttk.Treeview()
        self.XMLFile = ET.ElementTree(file=self.robot.get_uiautomator_dump())
        self.tree_info("", self.XMLFile)
        self.path_range = len(self.path_list[index])
        self.node_item = None
        self.Find_image_Path(index, 1, "")

        if self.node_item != None:
            self.ExistsImage(index)

    def ClickValue(self,index):
        #filePath = IMG_PATH(self.robot.screenshot())
        #self.photo = Image.open(filePath)
        self.treeview = ttk.Treeview()
        self.XMLFile = ET.ElementTree(file=self.robot.get_uiautomator_dump())
        self.tree_info("", self.XMLFile)
        self.path_range =len(self.path_list[index])
        self.node_item = None
        self.Find_image_Path(index, 1, "")

        if self.node_item != None:
            self.ClickImage(index)

    def ExistsImage(self, index):
        left, top, right, bottom = self.bounds_split(self.treeview.item(self.node_item)["values"][1])
        #img = self.photo.crop((left, top, right, bottom))
        #print(left, top, right, bottom)
        status = assert_finder(self.image[index],left, top, right, bottom)
        if status == True:
            print("Success : Find This Image and Node")
        else:
            print("Error : Not Find Image and Node")
            self.ActionError = True

    def ClickImage(self, index):
        left, top, right, bottom = self.bounds_split(self.treeview.item(self.node_item)["values"][1])
        # img = self.photo.crop((left, top, right, bottom))
        # print(left, top, right, bottom)
        status = template_finder(self.image[index],left, top, right, bottom)
        if status =="success":
            self.robot.tap((right + left)/2, (bottom + top)/2 )
            print((right + left)/2, (bottom + top)/2 )
        else:
            print("Error : Not Find Template Image")
            self.ActionError = True

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
                if self.path_list[index][depth-1][0] == self.treeview.item(child)["text"] :
                    print("find ", self.path_list[index][depth - 1][0],",  treeview node :", self.treeview.item(child)["text"])
                    depth = depth + 1
                    self.Find_image_Path(index, depth,child)
                else :
                    print("not find ", self.path_list[index][depth-1][0],",  treeview node :", self.treeview.item(child)["text"])

        if depth == self.path_range:
            children_node = self.treeview.get_children(item)
            for child in children_node:
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
        self.robot.drag_and_drop(int(X_start),int(Y_start),int(X_end),int(Y_end))
        print("Drag Coordinate is start x = ",int(X_start)," y = ",int(Y_start),"to  x = ",int(X_end)," y = ",int(Y_end))

    def InputValue(self, index):
        print(self.value[index])
        self.robot.input_text(self.value[index])

    def Send_Key_Value(self, index):
        self.robot.send_key(self.value[index])


