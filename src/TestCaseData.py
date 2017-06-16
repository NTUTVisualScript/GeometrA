from MessageUI import Message

class TestCaseData:
    def __init__(self):
        self.actionlist = []
        self.valuelist = []
        self.imagelist = []
        self.node_path_list = []
        self.loop_begin = []
        self.loop_end = []
        self.message = Message.getMessage(self)

    def clear_data(self):
        del self.actionlist[:]
        del self.valuelist[:]
        del self.imagelist[:]
        del self.node_path_list[:]
        del self.loop_begin[:]
        del self.loop_end[:]

    def set_data(self, actioncombolist, valuelist, valueImagelist, node_path_list, testcaseName = None):
        for i in range(len(actioncombolist)):
            self.actionlist.append(actioncombolist[i].get())
            if actioncombolist[i].get() == "Loop Begin":
                self.loop_begin.append(i)
            if actioncombolist[i].get() == "Loop End":
                self.loop_end.append(i)

            if valueImagelist[i] != None:
                self.valuelist.append(None)
            else:
                self.valuelist.append(valuelist[i].get())
            if i < len(valueImagelist):
                self.imagelist.append(valueImagelist[i])
                self.node_path_list.append(node_path_list[i])

        self.loop_end.reverse()
        self.check_data()
        return self.checkstatus

    def load_file_set_data(self, actioncombolist, valuelist, valueImagelist, node_path_list):
        for i in range(len(actioncombolist)):
            self.actionlist.append(actioncombolist[i])
            if actioncombolist[i] == "Loop Begin":
                self.loop_begin.append(i)
            if actioncombolist[i] == "Loop End":
                self.loop_end.append(i)

            if valueImagelist[i] != None:
                self.valuelist.append(None)
            else:
                self.valuelist.append(valuelist[i])
            if i < len(valueImagelist):
                self.imagelist.append(valueImagelist[i])
                self.node_path_list.append(node_path_list[i])

        self.loop_end.reverse()
        self.check_data()
        return self.checkstatus

    def get_data(self):
        return self.actionlist, self.valuelist, self.imagelist, self.node_path_list

    def check_data(self):
        self.checkstatus = True
        self.check_loop()

    def check_loop(self):
        if len(self.loop_begin) != len(self.loop_end) :
            statusstr = "Action Loop Status Error, maybe you loss loop begin or loop end\n"
            self.message.InsertText(statusstr)
            self.checkstatus = False


    def run_status(self, line, status , testcaseName):
        if status == "Error":
            statusstr = testcaseName + "Action " + str(line + 1) + " Status Error\n"
        else:
            statusstr = testcaseName + "Action " + str(line + 1) + " Status Success\n"

        self.message.InsertText(statusstr)
