# import unittest
#
# import os, shutil
#
# from GeometrA.src.Record import *
# from GeometrA.src.File.WorkSpace import WorkSpace
#
# RECORD_FILE = './tests/record.log'
#
# class RecordTestSuite(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         path = './tests/Project0'
#         if os.path.isdir(path):
#             shutil.rmtree(path, True)
#
#     def setUp(self):
#         self.recordFile = './tests/record.log'
#         self.path = os.getcwd()
#         shutil.copytree('./tests/File/Project0', './tests/Project0')
#
#     def tearDown(self):
#         if os.path.isfile(self.recordFile):
#             os.remove(self.recordFile)
#
#     def tearDown(self):
#         path = './tests/Project0'
#         if os.path.isdir(path):
#             shutil.rmtree('path', True)
#
#     def testExportLog(self):
#         p = ['Project0', {'Project0':{'Suite1': ['case1', 'case2'],
#                           'Suite2': ['case2']}}]
#         path = self.path
#         ws = WorkSpace(self.path, p)
#
#         exportLog(workspace = ws)
#         self.assertTrue(os.path.isfile(self.recordFile))
#
#     def testLog(self):
#         p = ['Project0', {'Project0':{'Suite1': ['case1', 'case2'],
#                           'Suite2': ['case2']}}]
#         path = self.path
#         ws1 = WorkSpace(self.path, p)
#
#         exportLog(workspace = ws1)
#
#         ws = WorkSpace()
#         loadLog(ws)
#
#         log = [os.getcwd() + '/tests/Project0/Project0.json']
#         self.assertEqual(log, ws.log())
