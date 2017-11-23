# Diary:

## Sprint #18 2017/08/23 ~ 2017/09/12

### 2017/08/25 13:30 ~ 17:00        By Patrick
    1. Complete the coverage of all unit tested class. 

    Next Step:
    1. Implement the contact between UI and domain.

### 2017/08/25 09:05 ~ 11:30        By Patrick
    1. Finished the implement of 'Loop' function.

    Next Step:
    1. Check and complete UT to let UT coverage up to 100%
    2. Implement the contact between UI and domain.

### 2017/08/24      By Patrick
    1. Finished redesign of 'Test Step', and the refactor.
    2. Change the test using 'run' to use 'execute', improve 14% running time.

    Next Step:
    1. Implement 'Loop' function.
    2. Implement the contact between UI and domain.

### * ~ 2017/08/23  * ~ 18      By Patrick
    1. Build jenkins CI server for this project. Jenkins will build automatically at 7 am every morning
    2. Fixed Executor 'TestCase' function bug.
    3. Finished most function for executor(except for 'Loop')

    Next Step:
    1. Redesign the usage of 'Test Step' and do the refactor of all code using it.
    2. Change the using of 'run' function to 'execute' function if possible, so I can improve the execute time of unit test(Cut the report part code, and implement a report function.)
    3. Implement 'Loop' function (maybe just call a function with a while loop inside another for loop)


----------------------------------------------------------

## Sprint 2017/07/18 ~ 2017/08/08
### Sprint Goal: refactor the Test Case

### 2017/08/05 10:56 ~ 16:30
    Try to make TestCase controller
    Next Step:
    1. Complete controller of test case.
    2. Complete all functions that needed for executor.


### 2017/08/02 15:00 ~ 17:55
    1. Complete run() function
    2. Do refactor of status from boolean to 'Success', 'Failed', and 'Error'
    Next Step:
    1. Complete all functions that needed for executor.

### 2017/07/27 16:30 ~ 17:29
    Finished 'runAll' function in Executor
    Next Step:
    1. complete all functions that needed for executor.

### 2017/07/25 14:13 ~ 17:42
    Finish FileLoader and Save prototype
    Executor run is done
    Next Step:
    1. add 'runAll' function
    2. complete all function that needed for executor, so unit tests can truly pass

### 2017/07/25 10:00 ~ 10:38
    study about how to save file and load file

### 2017/07/24 13:00 ~ 17:15
    make Executor:
        Finished action: Click, Drag, Set Text.
        Finished unittest: Click, Drag, Set Text.
    Next Step:
    1. Study how to load file as Test Case
    2. Finish TestCase and rest of actions.

### 2017/07/24 10:00 ~ 11:50
    Adding unit test for Step and TestCase

### 2017/07/19 17:00
    Try to use MVC to handle Test case issue
    Work on TestCaseUI, working to generate Case Block.

### 2017/07/19 18:13 ~ 19:02
    Finish the generateCaseBlock function.
    Next step:
    1. make undo and redo class
    2. complete the functions used in generateCaseBlock
