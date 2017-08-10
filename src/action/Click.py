import xml.etree.cElementTree as ET
from tkinter import ttk
from adb_roboot import ADBRobot
from cv2img import CV2Img
from finder.template_finder import TemplateFinder
from MessageUI import Message

def Click_image(source_image, x1,y1):
    source = CV2Img()
    source.load_file(source_image, 1)
    source.draw_circle( x1, y1)
    source.save(source_image)

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

class Click:
    def __init__(self):
        self.robot = ADBRobot()
        self.message = Message.getMessage(self)

    def ClickImage(self, image):
        status = template_finder(self.step_before_image, image)

        if status =="success":
            # self.message.InsertText("Success : Click Image\n")
            return "Success"
        elif status == "too more":
            return self.ClickValue()
        else:
            print("Error : Image Not Find")
            self.message.InsertText("Error : Image Not Find\n")
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

    def tree_info(self,id , treeinfo):
        for elem in treeinfo.findall('node'):
            if elem is None: return
            id_child = self.treeview.insert(id, "end", elem , text="(" + str(elem.get('index')) + ") "
                                                                   + str(elem.get('class')) + "  "
                                                                   ,  values=( str(elem.get('text')),str(elem.get('bounds'))) , open=True)
            self.tree_info(id_child, elem)

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