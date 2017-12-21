import unittest
import os, shutil

from VisualScript.src.File.Creator import Creator

class CreatorTestSuite(unittest.TestCase):
    def testNew(self):
        creator = Creator()
        info = {
            'project' : 'Project1',
            'suite' : 'Suite1',
            'case' : 'Case1',
            'path' : './'
        }
        creator.new(info)
        self.assertTrue(os.path.isdir('./Project1'))
        self.assertTrue(os.path.isdir('./Project1/Suite1'))
        self.assertTrue(os.path.isdir('./Project1/Suite1/Case1'))
        self.assertTrue(os.path.isfile('./Project1/Suite1/Case1/testcase.json'))
        shutil.rmtree('./Project1', True)
