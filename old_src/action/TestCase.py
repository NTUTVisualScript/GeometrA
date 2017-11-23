from LoadFile import LoadFile
from Viewtest import TestAdepter
from adb_roboot import ADBRobot


class TestCase:
    def __init__(self):
        self.robot = ADBRobot()

    def TestCasePath(self, index):
        testcase_load = LoadFile()
        testcase_load.Decoder_Json(self.value[index])

        name = self.value[index].split('/')
        foldername = str(name.pop())

        testcase = TestAdepter()
        actioncombo_list, value_list, valueImage_list, node_path_list = testcase_load.get_Loading_Data()
        testcase_status = testcase.load_file_set_data(actioncombo_list, value_list, valueImage_list, node_path_list)

        testcase.testcaseName = foldername + " : "

        if testcase_status:
            status, count = testcase.run_all()
        else:
            testcase.message.InsertText("The Test case have some problem, please check Test Case File : \n"+ self.value[index] +" !\n")

        return status, count
