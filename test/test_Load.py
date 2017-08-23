import unittest

import sys
sys.path.append('../src/Save')
sys.path.append('../src')
sys.path.append('../src/TestCase')

from Load import FileLoader

class FileLoaderTestSuite(unittest.TestCase):
    def testConstructer(self):
        f = FileLoader('./TestCase/Test')
        self.assertEqual('./TestCase/Test', f.folderPath)
        self.assertEqual('Test', f.folderName)
        self.assertEqual('Android Keycode', f.case.getSteps(0).getAction())
        self.assertEqual('KEYCODE_HOME', f.case.getSteps(0).getValue())
