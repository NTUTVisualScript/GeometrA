from tkinter import *
from tkinter.filedialog import asksaveasfilename
from PIL import Image

ImageType = [
    ('PNG', '*.png'),
    ]

class saveImg:

    def Save(self, screen, croprange):
        savefilepath = asksaveasfilename(initialdir = "/", filetypes=ImageType,title="Save the crop image as...")

        if savefilepath is None : return
        saveIMG = Image.open(screen)
        left, top, right, bottom, multiple = croprange

        left = left * multiple
        top = top * multiple
        right = right * multiple
        bottom = bottom * multiple

        print (str(left) + "\n" + str(top) + "\n" + str(right) + "\n" + str(bottom) )
        cropIMG = saveIMG.crop(( left , top, right, bottom))
        print(savefilepath)
        savePath = savefilepath + ".png"
        cropIMG.save(savePath)