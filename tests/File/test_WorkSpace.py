import unittest

import os, shutil
from VisualScript.src.File.WorkSpace import WorkSpace

class WorkSpaceTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        shutil.rmtree('./Project1', True)
        shutil.rmtree('./Project2', True)

    def setUp(self):
        shutil.copytree('./Project', './Project1')
        shutil.copytree('./Project', './Project2')
        self.path = os.getcwd()

    def tearDown(self):
        shutil.rmtree('./Project1', True)
        shutil.rmtree('./Project2', True)

    def testConstructor(self):
        p = ['Project1', {'Project1':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        path = self.path
        ws = WorkSpace(path, p)
        self.assertEqual("<class 'File.WorkSpace.WorkSpace'>", str(ws.__class__))
        self.assertEqual(1, len(ws.projects))
        self.assertEqual(True, 'Project1' in ws.projects)
    def testConstructorExcept(self):
        p = ['Project1', {'Project1':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        path = self.path + '/' + 'Project1'
        message = 'Project: "Project1" is not in the path'
        self.assertRaisesRegex(Exception, message, WorkSpace, path, p)

    def testGetJSON(self):
        p = ['Project1', {'Project1':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        ws = WorkSpace(self.path, p)
        self.assertEqual(p[1], ws.getJSON('Project1'))

    def testGetTreeJSON(self):
        p1 = ['Project1', {'Project1':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        p2 = ['Project2', {'Project2':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        ws = WorkSpace(self.path, p1)
        ws.add(self.path, p2)

        result = [
            {"text" : "Project1",
             "children" : [
                {"text" : "Suite1", "children" : [
                    {"text":"case1"},
                    {"text":"case2"}
                ]},
                {"text" : "Suite2", "children" : [
                    {"text":"case2"}
                ]}
             ]},
             {"text" : "Project2",
             "children" : [
                {"text" : "Suite1", "children" : [
                    {"text":"case1"},
                    {"text":"case2"}
                ]},
                {"text" : "Suite2", "children" : [
                    {"text":"case2"}
                ]}
             ]}
        ]

        self.assertEqual(result, ws.getTreeJSON())
