import unittest
import os
import sys
sys.path.append('../../src')

from File.Project import Project

class ProjectTestSuite(unittest.TestCase):
    def testConstructor(self):
        path = os.getcwd() + '/Project1'
        d = {'Suite1':['case1', 'case2'], 'Suite2':['case2']}
        project = Project(d)
        self.assertEqual("<class 'File.Project.Project'>", str(project.__class__))
        self.assertEqual(2, len(project.suites))
