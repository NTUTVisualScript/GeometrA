from cv2img import CV2Img
from adb_roboot import ADBRobot
from finder.template_finder import TemplateFinder
from finder.template_matcher import TemplateMatcher
from uiautomator import device as d
import time
import os

ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(ROOT_DIR, "screenshot_pic")

def IMG_PATH(name):
    return os.path.join(RESOURCES_DIR, name)

def template_finder(target_image):
    robot = ADBRobot()
    source = CV2Img()
    source.load_file(IMG_PATH(robot.screenshot()), 0)
    source.show()
    target = CV2Img()
    target.load_PILimage(target_image)
    target.show()
    finder = TemplateFinder(source)
    results = finder.find_all(target, 0.9)

    for item in results :
        coordinate_x, coordinate_y = source.coordinate(item)
        robot.tap(coordinate_x, coordinate_y)

def assert_finder(target_path):
    robot = ADBRobot()
    source = CV2Img()
    source.load_file(IMG_PATH(robot.screenshot()), -1)

    target = CV2Img()
    target.load_file(IMG_PATH(target_path), -1)

    ratio = min(target.rows / 12, target.cols / 12)

    matcher = TemplateMatcher(source, target, 1, ratio)
    result = matcher.next()

    result_image = source.crop(result)
    assert result_image == target

class TestAdepter():
    def Test(self, actioncomboboxlist, typecomboboxlist, valuelist, valueImagelist):
        self.robot = ADBRobot()
        self.action = []
        self.type = []
        self.value = []
        self.image = []

        print(len(actioncomboboxlist))
        for i in range(len(actioncomboboxlist)):
            self.action.append(actioncomboboxlist[i].get())
            self.type.append(typecomboboxlist[i].get())
            if valueImagelist[i] != None:
                print(valueImagelist[i])
                self.value.append(None)
            else:
                self.value.append(valuelist[i].get())

            if i < len(valueImagelist):
                self.image.append(valueImagelist[i])

        os.popen("adb kill-server")
        time.sleep(1)
        os.popen("adb devices")
        time.sleep(5)
        self.Action()

    def Action(self):
        index = 0
        for i in self.action:
            time.sleep(2)
            if str(i) == "":
                break
            if str(i) == "Click":
                print(index)
                self.ClickType(index)
            elif str(i) == "Drag":
                print(self.action.index(i))
                self.DragType(index)
            elif str(i) == "Assert":
                print(self.action.index(i))
                self.AssertType(index)
            index = index+1

    def ClickType(self,index):
        if self.type[index] == 'text':
            self.TextValue(index)

        elif self.type[index] == 'image':
            self.ImageValue(index)

        elif self.type[index] == 'coordinate':
            self.CoordinateValue(index)

    def DragType(self,index):
        if self.type[index] == 'coordinate':
            self.DragCoordinateValue(index)

    def AssertType(self,index):
        if self.type[index] == 'image':
            self.ImageValue(index)

    def TextValue(self,index):
        print(str(self.value[index]))
        textstr = str(self.value[index])
        print(textstr)
        d(text=textstr).click()

    def ImageValue(self,index):
        template_finder(self.image[index])

    def CoordinateValue(self,index):
        coordinatevalue = str(self.value[index])
        coordinate = coordinatevalue.split(",")
        X_coordinate = coordinate[0].split('=')
        X_value = X_coordinate[1]
        Y_coordinate = coordinate[1].split('=')
        Y_value = Y_coordinate[1]
        #self.robot.tap(int(int(X_value)),int(int(Y_value)))
        print("click Coordinate is x = ", int(int(X_value)), " , y = ", int(int(Y_value)))
        d.click(int (int(X_value)), int(int(Y_value)))


    def DragCoordinateValue(self,index):
        coordinatevalue = str(self.value[index])
        coordinate = coordinatevalue.split(",")
        X_coordinate_start = coordinate[0].split('=')
        X_start = X_coordinate_start[1]
        Y_coordinate_start = coordinate[1].split('=')
        Y_start = Y_coordinate_start[1]

        X_coordinate_end = coordinate[2].split('=')
        X_end = X_coordinate_end[1]
        Y_coordinate_end = coordinate[3].split('=')
        Y_end = Y_coordinate_end[1]
        #self.robot.drag_and_drop(int(X_start),int(Y_start),int(X_end),int(Y_end))
        d.drag(int(X_start) , int(Y_start) , int(X_end) , int(Y_end), steps=1000)
        print("Drag Coordinate is start x = ",int(X_start)," y = ",int(Y_start),"to  x = ",int(X_end)," y = ",int(Y_end))


