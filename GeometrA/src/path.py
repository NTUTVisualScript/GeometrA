import platform
import os

file_path = os.path.abspath(__file__)[0:]

if (platform.system() == 'Windows'):
    GEOMETRA_ROOT = os.environ['USERPROFILE'] + '\\.GeometrA'
    RESOURCE_PATH = file_path[0:file_path.rindex('\\', 0, file_path.rindex('\\', 0, file_path.rindex('\\')))] + '\\resources'
else:
    GEOMETRA_ROOT = os.environ['HOME'] + '/.GeometrA'
    RESOURCE_PATH = file_path[0:file_path.rindex('/', 0, file_path.rindex('/', 0, file_path.rindex('/')))] + '/resources'

if (not os.path.isdir(GEOMETRA_ROOT)):
    if (os.path.isfile(GEOMETRA_ROOT)):
        os.remove(GEOMETRA_ROOT)
    os.mkdir(GEOMETRA_ROOT)
