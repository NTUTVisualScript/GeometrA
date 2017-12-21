import unittest
import os, shutil


from VisualScript.src.File.Project import Project

class ProjectTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        shutil.rmtree('./Project1', True)

    def setUp(self):
        self.path = os.getcwd() + '/Project1'
        shutil.copytree('./Project', './Project1')

    def tearDown(self):
        shutil.rmtree('./Project1', True)

    def testConstructor(self):
        d = {'Suite1':['case1', 'case2'], 'Suite2':['case2']}
        project = Project(self.path, d)
        self.assertEqual("<class 'File.Project.Project'>", str(project.__class__))
        self.assertEqual(2, len(project.suites))
        self.assertEqual(self.path, project.path)
    def testConstructorNotExist(self):
        d = {'Suite3':['case1', 'case2'], 'Suite2':['case2']}
        project = Project(self.path, d)
        self.assertEqual("<class 'File.Project.Project'>", str(project.__class__))
        self.assertEqual(os.getcwd() + '/Project1/Suite2', project.suites['Suite2'].path)
        self.assertEqual(1, len(project.suites))
        self.assertEqual(self.path, project.path)

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
        self.assertTrue(os.path.isdir('./Project1/Suite 1'))
        self.assertFalse(os.path.isdir('./Project1/Suite1'))
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
               {"text":"case1"},
               {"text":"case2"}
           ]},
           {"text" : "Suite2", "children" : [
               {"text":"case2"}
           ]}
        ]
        project = Project(self.path, d)

        self.assertEqual(result, project.getTreeJSON())
