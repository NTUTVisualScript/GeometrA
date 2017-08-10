from cv2img import CV2Img
from adb_roboot import ADBRobot
from MessageUI import Message

def Drag_image(source_image, x1,y1,x2,y2):
    source = CV2Img()
    source.load_file(source_image, 1)
    source.draw_line(x1,y1,x2,y2)
    source.draw_circle(x2,y2)
    source.save(source_image)

class Drag:
    def __init__(self):
        self.robot = ADBRobot()
        self.message = Message.getMessage(self)

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