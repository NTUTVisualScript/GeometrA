# Overview of GeometrA

## Initialize Page
#### For the first time you use GeometrA, the system will automatically direct you to Initialize page. You have to either **load a project** or **create a new project**.

- Initialize Page:

![](/docs/pic/Initialize.PNG)

- Create Project Page:

![](/docs/pic/Create.PNG)

- Load Project Page:

![](/docs/pic/Load.PNG)

## Full view

![](/docs/pic/Fullview.png)

## Toolbar
#### Provides functional buttons for user to create/load/run their test scripts or to dump the current screen of the device.

![](/docs/pic/Toolbar.PNG)

## Work Space
#### You can manage the files and directories of your project in Work Space.

- Work Space:

![](/docs/pic/WorkSpace.PNG)

## Current Screen
#### Current Screen provides the view of current screen of testing device for user to interact with. User can interact with specific actions on Current Screen according to the selected action block of Editor.

- Current Screen view:

![](/docs/pic/Screen.PNG)

## Editor
#### Editor is made of [Blockly](https://developers.google.com/blockly/) api, in order to let users to write their tests as simple as drag and drop.
A test script of GeometrA contains several *action blocks* as their steps, and each step is composed of one action block and one corresponeding argument. User can select the action blocks they need from the toolbox on the left, and set the value of arguments to implement their test scripts.

- Editor:

![](/docs/pic/Editor.PNG)

- Image argument:

As the picture of Editor view above, there's several blocks -- Click, Assert Exist, Assert Not Exist -- use image as their arguments, in that way, people can easily know what the step is really doing. To set a *image argument*, user can simply crop the sub-image they want to assert from the current screen we've just introduced above.

![](/docs/pic/ImageArgument.gif)

- Swipe argument:
Besides, for *Swipe* action, user could also swipe on the current screen to get the value of the direction and distance user want easily and clearly.

![](/docs/pic/SwipeArgument.gif)

## Node Tree
#### Display the tree structure of object infomations of current screen of testing device. User can get the corresponeding image-argument from selecting the node of the tree.

- Node Tree

![](/docs/pic/NodeTree.png)

## Message
#### Show the loggin messages of the result of users operations or test executions.

- Message

![](/docs/pic/message.PNG)
