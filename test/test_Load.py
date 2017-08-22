import unittest

import sys
sys.path.append('../src/Save')
sys.path.append('../src')
sys.path.append('../src/TestCase')

from Load import FileLoader

class FileLoaderTestSuite(unittest.TestCase):
    def testConstructer(self):
        f = FileLoader('C:/Test')
        self.assertEqual('C:/Test', f.folderPath)
        self.assertEqual('Test', f.folderName)
