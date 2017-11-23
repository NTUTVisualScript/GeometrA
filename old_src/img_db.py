import os
import json
from cv2img import CV2Img
from rectangle import Rectangle

class ImgFile:
    def __init__(self, file_path, roi=None):
        self._path = file_path
        self._roi = roi

        dir_path = os.path.dirname(file_path)
        filename, file_extension = os.path.splitext(file_path)

        if os.path.exists(filename + ".json"):
            with open(filename + ".json", "r") as fp:
                self._map = json.loads(fp.read())
        else:
            self._map = None

    def load(self):
        img = CV2Img()
        img.load_file(self._path)

        if self._roi:
            img = img.crop(self._roi)

        return img

    def __getattr__(self, item):
        if self._map is None and "_subimages" not in self._map:
            return None

        subimage = self._map["_subimages"].get(item, None)
        if subimage is None:
            return None

        if "_roi" in subimage:
            roi = Rectangle(**subimage["_roi"])
        else:
            roi = None

        return ImgFile(self._path, roi)


class ImgDB:
    def __init__(self, root_dir):
        self._root = root_dir

    def __getattr__(self, item):
        # Folder
        path = os.path.join(self._root, item)

        if os.path.exists(path):
            if os.path.isdir(path):
                return ImgDB(path)

        # Picture
        path = os.path.join(self._root, item + ".png")
        if os.path.exists(path):
            if os.path.isfile(path):
                return ImgFile(path)
