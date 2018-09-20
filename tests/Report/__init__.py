import unittest
import os.path, shutil

from tests.Report.test_ReportUi import ReportUiTestSuite
from jinja2 import Environment, PackageLoader, select_autoescape

from GeometrA.src.Report import Report
# class TemplateTestSuite(unittest.TestCase):
#     def setUp(self):
#         self.env = Environment(
#             loader=PackageLoader('GeometrA', 'templates'),
#             autoescape=select_autoescape(['html', 'xml'])
#         )
#         self.template = self.env.get_template('Report/report.html')
#     def testTemplate(self):
#         print('*************************\nTest Template\n************************')
#         print(self.template)
#
#     def testRender(self):
#         print('*************************\nTest Render\n************************')
#         print(self.template.render(
#             projects = {
#                 'project': {
#                     'suite': {
#                         'cas1': 'success',
#                         'case2': 'failed'
#                     }
#                 }
#             },
#             serialNumber= "1", display= "1080 x 1920", date= "Today", count= 2
#         ))

class ReportTestSuite(unittest.TestCase):
    def setUp(self):
        self.report = Report()

    def tearDown(self):
        shutil.rmtree('./tests/Report/project1/report', True)

    def testGetReport(self):
        result = self.report.getReport()
        self.assertEqual(str(result.__class__), "<class 'str'>")

    def testAddCase(self):
        path1 = "./tests/Report/project1/suite1/case1"
        status = 'success'
        self.report.addCase(path1, status)
        self.assertEqual(self.report.projects, {
            "project1": {
                "suite1": {
                    "case1": status
                }
            }
        })
        path2 = './tests/Report/project1/suite1/case2'
        self.report.addCase(path2, status)
        self.assertEqual(self.report.projects, {
            "project1": {
                "suite1": {
                    "case1": status,
                    "case2": status
                }
            }
        })
        path3 = './tests/Report/project1/suite2/case1'
        self.report.addCase(path3, status)
        self.assertEqual(self.report.projects, {
            "project1": {
                "suite1": {
                    "case1": status,
                    "case2": status
                },
                "suite2": {
                    "case1": status
                }
            }
        })
        path4 = './tests/Report/project2/suite1/case1'
        self.report.addCase(path4
        , status)
        self.assertEqual(self.report.projects, {
            "project1": {
                "suite1": {
                    "case1": status,
                    "case2": status
                },
                "suite2": {
                    "case1": status
                }
            },
            "project2": {
                "suite1": {
                    "case1": status
                }
            }
        })

    def testGetReportPath(self):
        path1 = "./tests/Report/project1/suite1/case1"
        status = 'success'
        self.report.addCase(path1, status)
        self.assertEqual(self.report.getReportPath(), './tests/Report/project1/report')

    def testGenerateReport(self):
        path1 = "./tests/Report/project1/suite1/case1"
        status = 'success'
        self.report.addCase(path1, status)
        self.report.generate()
        reportPath = "./tests/Report/project1/report"
        self.assertEqual(os.path.exists(reportPath), True)
