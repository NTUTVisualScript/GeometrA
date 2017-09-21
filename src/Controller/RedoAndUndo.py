from TestCaseUI import TestCaseUI

class RedoAndUndo():
    def __init__(self):
        self.testcase_undo = []
        self.testcase_redo = []

    def Undo(self):
        if len(self.testcase_undo) != 0:
            print("undo " + str(self.testcase_undo))
            testcase_line = self.testcase_undo.pop()
            line = testcase_line[0]

            if str(type(self.valuelist[line])) == "<class 'TestCaseEntry.TestCaseValue'>":
                add_redo = [line, "", self.actioncombolist[line].get(), self.valuelist[line].get(),
                            self.valueImagelist[line], self.node_path_list[line]]
            else:
                add_redo = [line, "", self.actioncombolist[line].get(), self.valuelist[line].image,
                            self.valueImagelist[line], self.node_path_list[line]]

            self.testcase_redo.append(add_redo)

            print(line)
            if testcase_line[1] == "remove":
                self.AddLineButtonClick(line, True)
                self.actioncombolist[line].set(testcase_line[2])
                self.actionlist[line] = testcase_line[2]
                print("undo ", testcase_line[2])
                if testcase_line[2] == "Click" or testcase_line[2] == "Assert Exist" or \
                     testcase_line[2] == "Assert Not Exist":
                    self.TestcaseImage(line, testcase_line[3])
                else:
                    self.TestcaseEntry(line)
                    self.valuelist[line].delete(0, END)
                    self.valuelist[line].insert(0, testcase_line[3])

            elif testcase_line[1] == "add":
                self.RemoveLineButtonClick(line, True)
            elif testcase_line[2] == "Click" or testcase_line[2] == "Assert Exist" or \
                            testcase_line[2] == "Assert Not Exist":
                self.actioncombolist[line].set(testcase_line[2])
                self.TestcaseImage(line, testcase_line[3])
            else:
                self.TestcaseEntry(line)
                self.actioncombolist[line].set(testcase_line[2])
                self.valuelist[line].delete(0, END)
                if testcase_line[3]!= None:
                   self.valuelist[line].insert(0, testcase_line[3])

            self.valueImagelist[line] = testcase_line[4]
            self.node_path_list[line] = testcase_line[5]

    def Redo(self):
        if len(self.testcase_redo) != 0:
            print("redo " + str(self.testcase_redo))
            testcase_line = self.testcase_redo.pop()
            line = testcase_line[0]

            if str(type(self.valuelist[line])) == "<class 'TestCaseEntry.TestCaseValue'>":
                add_undo = [line, "", self.actioncombolist[line].get(), self.valuelist[line].get(), self.valueImagelist[line], self.node_path_list[line]]
            else:
                add_undo = [line, "", self.actioncombolist[line].get(), self.valuelist[line].image, self.valueImagelist[line], self.node_path_list[line]]

            self.testcase_undo.append(add_undo)

            self.actioncombolist[line].set(testcase_line[2])
            if testcase_line[1] == "remove":
                self.RemoveLineButtonClick(line, True)
            elif testcase_line[1] == "add":
                self.AddLineButtonClick(line, True)
            elif testcase_line[2] == "Click" or testcase_line[2] == "Assert Exist" or \
                            testcase_line[2] == "Assert Not Exist":
                self.TestcaseImage(line, testcase_line[3])
            else:
                self.TestcaseEntry(line)
                self.valuelist[line].delete(0, END)
                if testcase_line[3] != None:
                    self.valuelist[line].insert(0, testcase_line[3])

            self.valueImagelist[line] = testcase_line[4]
            self.node_path_list[line] = testcase_line[5]

    def AddLineButtonClick(self,n, redoundo ):
        if redoundo ==False:
            self.add_changes( n, "add", self.actionlist[n], self.valuelist[n], self.valueImagelist[n],
                            self.node_path_list[n])

        self.line  = self.line + 1
        self.new_line(self.line)
        i= self.line

        self.valueImagelist.insert(n, None)
        self.node_path_list.insert(n, None)

        while i > n:
            getactionstr = self.actioncombolist[i-1].get()
            self.actioncombolist[i].set(str(getactionstr))
            self.actioncombolist[i-1].set('')
            self.actionlist[i] = self.actionlist[i-1]
            self.actionlist[i-1] = ""

            if str(type(self.valuelist[i-1])) != "<class 'TestCaseEntry.TestCaseValue'>":
                self.TestcaseImage(i, self.valuelist[i-1].image)
                self.TestcaseEntry(i-1)

            else:
                getvaluestr = self.valuelist[i-1].get()
                self.valuelist[i].delete(0, 'end')
                self.valuelist[i].insert('end', getvaluestr)
                self.valuelist[i - 1].delete(0, 'end')

            i=i-1


    def RemoveLineButtonClick(self, n, do):
        if do == False:
            self.add_changes(n, "remove", self.actionlist[n], self.valuelist[n], self.valueImagelist[n],
                            self.node_path_list[n])

        del self.valueImagelist[n]
        del self.node_path_list[n]
        i = n
        while i < self.line:
            getactionstr = self.actioncombolist[i + 1].get()
            self.actioncombolist[i].set(str(getactionstr))
            self.actionlist[i] = self.actionlist[i + 1]
            self.actionlist[i + 1] = ""

            if str(type(self.valuelist[i+1])) != "<class 'TestCaseEntry.TestCaseValue'>":
                self.TestcaseImage(i, self.valuelist[i+1].image)
                self.TestcaseEntry(i+1)

            else:
                self.TestcaseEntry(i)
                getvaluestr = self.valuelist[i+1].get()
                self.valuelist[i].delete(0, 'end')
                self.valuelist[i].insert('end', getvaluestr)
                self.valuelist[i+1].delete(0, 'end')

            i = i + 1

        self.lineStrlist[self.line].grid_remove()
        self.actioncombolist[self.line].grid_remove()
        self.valuelist[self.line].grid_remove()
        self.addlinelist[self.line].grid_remove()
        self.removelinelist[self.line].grid_remove()
        self.run_single_actionlist[self.line].grid_remove()

        self.lineStrlist.pop()
        self.actioncombolist.pop()
        self.valuelist.pop()
        self.addlinelist.pop()
        self.removelinelist.pop()
        self.run_single_actionlist.pop()
        self.line = self.line - 1
