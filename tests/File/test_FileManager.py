import unittest
import os, shutil

from GeometrA.src.File.FileManager import *
from GeometrA.src.File.WorkSpace import WorkSpace

class FileManagerTestSuite(unittest.TestCase):
    def setUp(self):
        if os.path.isdir('./tests/Project1'):
            shutil.rmtree('./tests/Project1')

    def testNew(self):
        info = {
            'project' : 'Project1',
            'suite' : 'Suite1',
            'case' : 'Case1',
            'path' : './tests',
        }
        new(info)
        self.assertTrue(os.path.isdir('./tests/Project1'))
        self.assertTrue(os.path.isdir('./tests/Project1/Suite1'))
        self.assertTrue(os.path.isdir('./tests/Project1/Suite1/Case1'))
        # self.assertTrue(os.path.isfile('./tests/Project1/Suite1/Case1/testcase.json'))
        self.assertTrue(os.path.isfile('./tests/Project1/Project1.json'))
        shutil.rmtree('./tests/Project1', True)

    def testNewException(self):
        info = {
            'project' : 'TestCase',
            'suite': 'Suite1',
            'case': 'Case1',
            'path': './tests',
        }

        self.assertRaisesRegex(Exception, 'The directory is exist!', new, info)

    def testLoad(self):
        path = './tests/File/Project0/Project0.json'
        path2 = './tests/File'
        p = ['Project', {'Project':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        ws = WorkSpace(path2, p)
        ans = ['Project0', {'Project0':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        load(path, ws)
        self.assertEqual(ans, ws.getJSON('Project0'))

    def testLoadException(self):
        path = './tests/File/ErrorProject/Project0.json'
        path2 = './tests/File'
        p = ['Project', {'Project':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        ws = WorkSpace(path2, p)

        self.assertRaisesRegex(Exception, 'Project: Projct is not in the path')
