import unittest

import os, shutil, json
from VisualScript.src.File.WorkSpace import WorkSpace
from xml.etree import ElementTree as ET

class WorkSpaceTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.path.isdir('./File/Project1'):
            shutil.rmtree('./File/Project1', True)
        if os.path.isdir('./File/Project2'):
            shutil.rmtree('./File/Project2', True)
        if os.path.isdir('./File/Project3'):
            shutil.rmtree('./File/Project3', True)

    def setUp(self):
        shutil.copytree('./File/Project', './File/Project1')
        shutil.copytree('./File/Project', './File/Project2')
        self.path = os.getcwd() + '/File'
        with open (self.path + '/Project1/Project1.json', 'w') as f:
            data = [
                "Project1",
                {
                    "Project1":{
                        "Suite1": ["case1", "case2"],
                        "Suite2": ["case2"]
                    }
                }
            ]
            f.write(json.dumps(data))
        with open (self.path + '/Project2/Project2.json', 'w') as f:
            data = [
                "Project2",
                {
                    "Project2":{
                        "Suite1": ["case1", "case2"],
                        "Suite2": ["case2"]
                    }
                }
            ]
            f.write(json.dumps(data))

    def tearDown(self):
        if os.path.isdir('./File/Project1'):
            shutil.rmtree('./File/Project1', True)
        if os.path.isdir('./File/Project2'):
            shutil.rmtree('./File/Project2', True)
        if os.path.isdir('./File/Project3'):
            shutil.rmtree('./File/Project3', True)

    def testConstructor(self):
        p = ['Project1', {'Project1':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        path = self.path
        ws = WorkSpace(path, p)
        self.assertEqual("<class 'VisualScript.src.File.WorkSpace.WorkSpace'>", str(ws.__class__))
        self.assertEqual(1, len(ws.projects))
        self.assertEqual(True, 'Project1' in ws.projects)
    def testConstructorExcept(self):
        p = ['Project1', {'Project1':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        path = self.path + '/' + 'Project1'
        message = 'Project: "Project1" is not in the path'
        self.assertRaisesRegex(Exception, message, WorkSpace, path, p)

    def testLoad(self):
        p1 = ['Project1', {'Project1':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        p2 = ['Project2', {'Project2':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        ws = WorkSpace(self.path, p1)
        ws.load(self.path, p2)
        self.assertEqual(p2, ws.getJSON('Project2'))

    def testAdd(self):
        p1 = ['Project1', {'Project1':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        ws = WorkSpace(self.path, p1)
        ws.add(self.path, 'Project3')
        p3 = ['Project3', {'Project3':{}}]
        self.assertEqual(p3, ws.getJSON('Project3'))
        self.assertTrue(os.path.isdir('./File/Project3'))
        self.assertTrue(os.path.isfile('./File/Project3/Project3.json'))
    def testAddException(self):
        p1 = ['Project1', {'Project1':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        ws = WorkSpace(self.path, p1)
        message = 'Project: "Project1" is already exists!'
        self.assertRaisesRegex(Exception, message, ws.add, self.path, 'Project1')

    def testDelete(self):
        p1 = ['Project1', {'Project1':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        ws = WorkSpace(self.path, p1)
        ws.add(self.path, 'Project3')
        ws.delete('Project3')
        message = 'Project: "Project3" not exist'
        self.assertRaisesRegex(Exception, message, ws.getJSON, 'Project3')
        self.assertFalse(os.path.isdir('./File/Project3'))

    def testRename(self):
        p1 = ['Project1', {'Project1':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        ws = WorkSpace(self.path, p1)
        ws.rename('Project1', 'Project3')
        p3 = ['Project3', {'Project3':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]

        self.assertFalse('Project1' in ws.projects)
        self.assertEqual(p3, ws.getJSON('Project3'))
        self.assertEqual(self.path + '/Project3', ws.projects['Project3'].path)
        self.assertEqual(self.path + '/Project3/Suite2', ws.projects['Project3'].suites['Suite2'].path)
        self.assertTrue(os.path.isdir('./File/Project3'))
        self.assertFalse(os.path.isdir('./File/Project1'))
        self.assertTrue(os.path.isfile('./File/Project3/Project3.json'))

    def testGetJSON(self):
        p = ['Project1', {'Project1':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        ws = WorkSpace(self.path, p)
        self.assertEqual(p, ws.getJSON('Project1'))

    def testGetTreeJSON(self):
        p1 = ['Project1', {'Project1':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        ws = WorkSpace(self.path, p1)

        result = [
            {"text" : "Project1",
             "children" : [
                {"text" : "Suite1", "children" : [
                    {"text":"case1", "type": "itsfile"},
                    {"text":"case2", "type": "itsfile"}
                ]},
                {"text" : "Suite2", "children" : [
                    {"text":"case2", "type": "itsfile"}
                ]}
             ]}
        ]

        self.assertEqual(result, ws.getTreeJSON())

    def testLog(self):
        p = ['Project1', {'Project1':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        path = self.path
        ws = WorkSpace(path, p)
        ans = [self.path + '/' + p[0] + '/' + p[0] + '.json']
        self.assertEqual(ans, ws.log())

    def testSave(self):
        xml = '''
            <xml xmlns="http://www.w3.org/1999/xhtml">
            <variables></variables>
            <block type="main" id="MvP*eIp|Z5#uW};@Q}^$" x="162" y="36">
                <next>
                    <block type="sleep" id="C-ko,K})FR1SZLwgXF;p"><field name="Time">0</field></block>
                </next>
            </block>
            </xml>
        '''
        code = "Main;Sleep(s),1"
        p = [
            "Project1",
            {
                "Project1":{
                    "Suite1": ["case1", "case2"],
                    "Suite2": ["case2"]
                }
            }
        ]
        focus = {
            "Project":"Project1",
            "Suite":"Suite1",
            "Case":"case1"
        }
        ws = WorkSpace(self.path, p)
        ws.setFocus(focus)
        ws.save(xml, code)
        with open(self.path + "/Project1/Suite1/case1/testcase.xml", 'r') as f:
            result = f.read()
        self.assertEqual(xml, result)
        with open(self.path + "/Project1/Suite1/case1/testcase.json", 'r') as f:
            result = f.read()
        ans ='{"Main": {"1": {"Action": "Sleep(s)", "Value": "1"}}}'
        self.assertEqual(ans, result);

    def testGetFocusPath(self):
        focus = {
            'Project': 'Project1',
            'Suite': 'Suite1',
            'Case': 'case1',
        }
        p = ['Project1', {'Project1':{'Suite1': ['case1', 'case2'],
                          'Suite2': ['case2']}}]
        path = self.path
        ws = WorkSpace(path, p)
        ws.setFocus(focus)
        self.assertEqual(path + '/Project1/Suite1/case1', ws.getFocusPath())

    def testOpen(self):
        xml = '''
            <xml xmlns="http://www.w3.org/1999/xhtml">
            <variables></variables>
            <block type="main" id="MvP*eIp|Z5#uW};@Q}^$" x="162" y="36">
                <next>
                    <block type="sleep" id="C-ko,K})FR1SZLwgXF;p"><field name="Time">0</field></block>
                </next>
            </block>
            </xml>
        '''
        code = "Main; Sleep(s), 1"
        p = [
            "Project1",
            {
                "Project1":{
                    "Suite1": ["case1", "case2"],
                    "Suite2": ["case2"]
                }
            }
        ]
        focus = {
            "Project":"Project1",
            "Suite":"Suite1",
            "Case":"case1"
        }
        ws = WorkSpace(self.path, p)
        ws.setFocus(focus)
        ws.save(xml, code)
        result = ws.open()
        self.assertEqual(xml, result)
