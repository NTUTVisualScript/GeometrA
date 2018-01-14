import unittest
import os, shutil

from VisualScript.src.File.FileManager import *

class FileManagerTestSuite(unittest.TestCase):
    def testNew(self):
        info = {
            'project' : 'Project1',
            'suite' : 'Suite1',
            'case' : 'Case1',
            'path' : './',
        }
        new(info)
        self.assertTrue(os.path.isdir('./Project1'))
        self.assertTrue(os.path.isdir('./Project1/Suite1'))
        self.assertTrue(os.path.isdir('./Project1/Suite1/Case1'))
        self.assertTrue(os.path.isfile('./Project1/Suite1/Case1/testcase.json'))
        self.assertTrue(os.path.isfile('./Project1/Project1.json'))
        shutil.rmtree('./Project1', True)

    def testNewException(self):
        info = {
            'project' : 'TestCase',
            'suite': 'Suite1',
            'case': 'Case1',
            'path': './',
        }

        self.assertRaisesRegex(Exception, 'The directory is exist!', new, info)

    def testLoad(self):
        path = './File/Project0'
        path2 = './File/Project'
        p = ['Project', {'Project':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        ws = WorkSpace(path2, p)

        self.assertTrue(load(path, workspace=ws))
