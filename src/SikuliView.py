from tkinter import *
from adb_roboot import ADBRobot
from PIL import Image, ImageTk
import os

ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources/taipeibus")

filePath = None
dumpfilePath = None

def IMG_PATH(name):
    return os.path.join(RESOURCES_DIR, name)

def Get_PhoneScreen():
    global filePath
    robot = ADBRobot()
    filePath = IMG_PATH(robot.screenshot())
    print(filePath)
    return filePath

def Dump_UI():
    global dumpfilePath
    robot = ADBRobot()
    dumpfilePath = IMG_PATH(robot.get_uiautomator_dump())
    print(dumpfilePath)
    return dumpfilePath

class View(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.photo = Image.open(Get_PhoneScreen())

        self.photo_width, self.photo_height = self.photo.size
        print(str(self.photo_width) +" , " + str(self.photo_height))

        self.photo.thumbnail((500, 800))

        self.width, self.height = self.photo.size
        self.resize = self.photo_width / self.width
        #self.photo_height_resize = self.photo_height / self.height

        print(str(self.resize))

        self.screenshot = Canvas(self.master, bg='white', height=self.height-1, width=self.width-1)
        self.screenshot.grid(row=0, column=0, rowspan=self.height, columnspan = self.width)
        self.screenshot_photo = ImageTk.PhotoImage(self.photo)
        self.screenshot.create_image(0, 0, anchor=NW, image=self.screenshot_photo)

        self.textbox = Text(self.master, height=30, width=80, wrap='word')
        vertscroll = Scrollbar(self.master)
        vertscroll.config(command=self.textbox.yview)
        self.textbox.config(yscrollcommand=vertscroll.set)
        self.textbox.grid(column=self.width + 1, row=0, rowspan=30, columnspan=80)
        vertscroll.grid(column=self.width + 82, row=0, rowspan=30, columnspan=1, sticky='NS')

        self.mousePosition = StringVar()  # displays mouse position
        self.mousePosition.set("Mouse outside window")
        self.positionLabel = Label(self.master, textvariable=self.mousePosition)
        self.positionLabel.grid(column=self.width + 1, row=32,columnspan=80)
        self.screenshot.bind("<Button-1>", self.clickdown) #clickdown
        self.screenshot.bind("<ButtonRelease-1>", self.clickup) #clickup
        #self.screenshot.bind("<Enter>", self.enteredWindow)
        #self.screenshot.bind("<Leave>", self.exitedWindow)
        self.screenshot.bind("<B1-Motion>", self.mouseDragged)

        self.canvas = Canvas(self.master, bg='white', width=200, height=200)
        self.canvas.grid(column=self.width + 1 , row=35)

    def clickdown(self, event):
        self.screenshot.create_image(0, 0, anchor=NW, image=self.screenshot_photo)
        self.mousePosition.set("Pressed at [ " + str(event.x) + ", " + str(event.y) + " ]")

        self.clickstartX = event.x
        self.clickstartY = event.y

    def clickup(self, event):
        self.clickendX = event.x
        self.clickendY = event.y

        left, right = sorted([self.clickendX, self.clickstartX])
        top, bottom = sorted([self.clickstartY, self.clickendY])

        self.cropped = self.photo.crop((left, top, right, bottom))
        #time.sleep(2)
        self.cropped.thumbnail((200, 200))
        #self.cropped.show()
        #
        self.tk_im = ImageTk.PhotoImage(self.cropped)
        self.canvas.create_image(0, 0, anchor=NW,image=self.tk_im)


    #def enteredWindow(self, event):
        #self.mousePosition.set("Mouse in window")

    #def exitedWindow(self, event):
        #self.mousePosition.set("Mouse outside window")

    def mouseDragged(self, event):
        self.screenshot.create_image(0, 0, anchor=NW, image=self.screenshot_photo)
        if event.x < 0 :
            event.x = 0 + 3
        if event.y < 0 :
            event.y = 0 + 3
        if event.x > self.screenshot_photo.width():
            event.x = self.screenshot_photo.width()-3
        if event.y > self.screenshot_photo.height():
            event.y = self.screenshot_photo.height()-3
        self.screenshot.create_rectangle(self.clickstartX, self.clickstartY, event.x, event.y, outline='red' ,width = 2)
        self.mousePosition.set("Rectangle at [ " + str(self.clickstartX * self.resize ) + ", " + str(self.clickstartY * self.resize) + " To " + str(event.x * self.resize) + ", " + str(event.y * self.resize) + " ]")



if __name__ == '__main__':
    root = Tk()
    root.title("Sikuli Viewer")
    app = View(master=root)
    app.mainloop()