import os

ROOT_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")

def IMG_PATH(name):
    return os.path.join(RESOURCES_DIR, name)



