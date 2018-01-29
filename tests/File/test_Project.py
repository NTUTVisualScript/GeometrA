import unittest
import os, shutil
import json

from VisualScript.src.File.Project import Project

class ProjectTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        shutil.rmtree('./File/Project1', True)

    def setUp(self):
        self.path = os.getcwd() + '/File/Project1'
        shutil.copytree('./File/Project', './File/Project1')

    def tearDown(self):
        shutil.rmtree('./File/Project1', True)

    def testConstructor(self):
        d = {'Suite1':['case1', 'case2'], 'Suite2':['case2']}
        project = Project(self.path, d)
        self.assertEqual("<class 'VisualScript.src.File.Project.Project'>", str(project.__class__))
        self.assertEqual(2, len(project.suites))
        self.assertEqual(self.path, project.path)
    def testConstructorNotExist(self):
        d = {'Suite3':['case1', 'case2'], 'Suite2':['case2']}
        project = Project(self.path, d)
        self.assertEqual("<class 'VisualScript.src.File.Project.Project'>", str(project.__class__))
        self.assertEqual(os.getcwd() + '/File/Project1/Suite2', project.suites['Suite2'].path)
        self.assertEqual(1, len(project.suites))
        self.assertEqual(self.path, project.path)

    def testAdd(self):
        d = {'Suite1':['case1', 'case2'], 'Suite2':['case2']}
        project = Project(self.path, d)
        project.add("Suite3")
        result = {'Suite1':['case1', 'case2'], 'Suite2':['case2'], 'Suite3':[]}
        self.assertEqual(result, project.getJSON())
        self.assertTrue(os.path.isdir('./File/Project1/Suite3'))
        self.assertTrue(os.path.isfile('./File/Project1/Project1.json'))

        with open ('./File/Project1/Project1.json', 'r') as f:
            data = json.load(f)
        recordResult = [
            'Project1',
            {
                'Project1': {
                    'Suite1': ['case1', 'case2'],
                    'Suite2': ['case2'],
                    'Suite3': []
                }
            }
        ]
        self.assertEqual(recordResult, data)

    def testAddCase(self):
        d = {'Suite1':['case1', 'case2'], 'Suite2':['case2']}
        project = Project(self.path, d)
        project.add("Suite1", "case3")
        result = {'Suite1':['case1', 'case2', 'case3'], 'Suite2':['case2']}
        self.assertEqual(result, project.getJSON())
        self.assertTrue(os.path.isdir('./File/Project1/Suite1/case3'))
        self.assertTrue(os.path.isfile('./File/Project1/Suite1/case3/case3.json'))
    def testAddException(self):
        d = {'Suite1':['case1', 'case2'], 'Suite2':['case2']}
        project = Project(self.path, d)
        message = 'Suite: "Suite1" is already exists!'
        self.assertRaisesRegex(Exception, message, project.add, 'Suite1')

    def testDelete(self):
        d = {'Suite1':['case1', 'case2'], 'Suite2':['case2']}
        project = Project(self.path, d)
        project.delete('Suite1')
        self.assertFalse('Suite1' in project.suites)
        self.assertFalse(os.path.isdir('./Project1/Suite1'))
    def testDeleteExcept(self):
        d = {'Suite1':['case1', 'case2'], 'Suite2':['case2']}
        project = Project(self.path, d)
        self.assertRaises(KeyError, project.delete, 'Suite')

    def testRename(self):
        d = {'Suite1':['case1', 'case2'], 'Suite2':['case2']}
        project = Project(self.path, d)
        project.rename('Suite1', 'Suite 1')
        self.assertFalse('Suite1' in project.suites)
        self.assertTrue('Suite 1' in project.suites)
        self.assertTrue(os.path.isdir('./File/Project1/Suite 1'))
        self.assertFalse(os.path.isdir('./File/Project1/Suite1'))
    def testRenameExcept(self):
        d = {'Suite1':['case1', 'case2'], 'Suite2':['case2']}
        project = Project(self.path, d)
        origin = 'Suite3'
        new = 'Suite'
        self.assertRaises(KeyError, project.rename, origin, new)
    def testRenameExistExcept(self):
        d = {'Suite1':['case1', 'case2'], 'Suite2':['case2']}
        project = Project(self.path, d)
        origin = 'Suite1'
        new = 'Suite2'
        self.assertRaisesRegex(Exception, 'Suite already exists', project.rename, origin, new)

    def testGetJSON(self):
        d = {'Suite1':['case1', 'case2'], 'Suite2':['case2']}
        project = Project(self.path, d)
        self.assertEqual(d, project.getJSON())

    def testGetTreeJSON(self):
        d = {'Suite1':['case1', 'case2'], 'Suite2':['case2']}
        result = [
           {"text" : "Suite1", "children" : [
               {"text":"case1", 'type': 'itsfile'},
               {"text":"case2", 'type': 'itsfile'}
           ]},
           {"text" : "Suite2", "children" : [
               {"text":"case2", 'type': 'itsfile'}
           ]}
        ]
        project = Project(self.path, d)

        self.assertEqual(result, project.getTreeJSON())
