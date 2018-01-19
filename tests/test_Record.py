import unittest

import os, shutil

from VisualScript.src.Record import *
from VisualScript.src.File.WorkSpace import WorkSpace

RECORD_FILE = './record.log'

class RecordTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        shutil.rmtree('./Project0', True)

    def setUp(self):
        self.recordFile = './record.log'
        self.path = os.getcwd()
        shutil.copytree('./File/Project0', './Project0')

    def tearDown(self):
        shutil.rmtree('./Project0', True)

    def testExportLog(self):
        p = ['Project0', {'Project0':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        path = self.path
        ws = WorkSpace(self.path, p)

        exportLog(workspace = ws)
        self.assertTrue(os.path.isfile(self.recordFile))
        os.remove(self.recordFile)

    def testLog(self):
        log = {
            'WorkSpace': self.path + '/Project0/Project0.json'
        }
        with open('./record.log', 'w') as f:
            f.write(str(log).replace("'", '"'))

        ws = WorkSpace()
        loadLog(ws)

        self.assertEqual([log['WorkSpace']], ws.log())
