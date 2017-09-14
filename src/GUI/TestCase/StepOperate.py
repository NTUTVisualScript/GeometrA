import Value

def insert(stepList, n):
    i = len(stepList)-1
    for i in range(len(stepList)-1, n, -1):
        action = stepList[i-1].action.get()
        stepList[i].action.set(str(action))
        stepList[i-1].action.set('')

        if str(stepList[i-1].value.__class__) != "<class 'TestCaseEntry.TestCaseValue'>":
            from TestCaseUI import TestCaseUI
            Value.testCaseImage(stepList, i, stepList[i-1].value.image)
            Value.testCaseEntry(stepList, i-1)
        elif (action == '') or (action == 'Loop End'):
            stepList[i].value.grid_remove()
        else:
            Value.testCaseEntry(stepList, i)
            value = stepList[i-1].value.get()
            stepList[i].value.delete(0, 'end')
            stepList[i].value.insert('end', value)

    stepList[n].value.grid_remove()

def remove(stepList, n):
    for i in range(n, len(stepList)-1):
        action = stepList[i+1].action.get()
        stepList[i].action.set(str(action))

        if str(stepList[i+1].value.__class__) != "<class 'TestCaseEntry.TestCaseValue'>":
            from TestCaseUI import TestCaseUI
            Value.testCaseImage(stepList, i, stepList[i+1].value.image)
            Value.testCaseEntry(stepList, i+1)
        elif (action == '') or (action == 'Loop End'):
            stepList[i].value.grid_remove()
            stepList[i].showImage.grid_remove()
        else:
            Value.testCaseEntry(stepList, i)
            value = stepList[i+1].value.get()
            stepList[i].value.delete(0, 'end')
            stepList[i].value.insert(0, value)

    stepList[len(stepList)-1].remove()
    stepList.pop()
