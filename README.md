Visual Script is a tool for users to write automated acceptance test for applications on Android applications.

# Old Version
[1.0](https://github.com/NTUTVisualScript/Visual_Script/tree/Old_Version)

# How to start

1.[Clone the project](https://github.com/NTUTVisualScript/Visual_Script.git)

2.Install [Python3](https://www.python.org/downloads/)  

    Check: "The version SHOULD BE **3** !!"

3.On Windows: *Execute "auto.bat" as administrator*

\tOn Mac OS: *Execute the following command in terminal of the path of the project*

    sh setup.sh

\tOr follow the "Environmental Setting"

4.

    python -m VisualScript.api

6.Connect to "http://127.0.0.1:5000/VisualScript"


# Environmental Setting

1.Install PIL  

    pip install Pillow

2.Install opencv3  

    pip install opencv_python


3.Install Flask

    pip install flask

4.Install flask-cors

    pip install -U flask-cors


## Windows

5.Set environment variable  

    Variable    Android_HOME    
    Value   Android SDK 的安裝路徑  

![](/pic/Environmental.PNG)

6.Install [Android Studio](https://developer.android.com/studio/index.html)

7.Set environment variable path  

    Variable    Path    
    Value   %Android_HOME%\platform-tools  

![](/pic/SystemPath.PNG)

## Mac OS (OS X)

5.Install brew: If you don't got one.

    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

6.Install ADB

    brew install android-platform-tools


## Interface Introduction

![](/pic/View_Introduction.png)

	================================
	Dump UI Button sends adb command to android device
	1. adb shell screencap
	2. adb shell uiautomator dump

    Display the picture on Screenshot View.
    Analysis the xml file and display the information on Tree View.
	================================
	+ Button
    Insert a line.
	================================
	- Button
    Delete a line.
	================================
	▶ Button
    Execute a step.
	================================
	Run Button
    Execute the test case.
	================================
	Reset TestCase Button
    Delete all steps.
	================================
	Action Combobox
	Select the action of the step.  
	================================
	Values Text
    Input the value according to the action.



## Test Action Introduction.
### Click
Click a spot of the android device.

Click a node on Tree View as the value to click.
![](/pic/Click.gif)

Drag and drop on Screenshot View to crop a image as value.
![](/pic/Click2.gif)


### Swipe
Swipe on the device.
![](/pic/Drag.gif)

### Set Text
Input a string on the device.
![](/pic/Input.gif)

### Android Keycode

![](/pic/Send_key.gif)


Execute ADB command according to the keycode.

[Keycode List](https://developer.android.com/reference/android/view/KeyEvent.html)

	0 -->  "KEYCODE_UNKNOWN"
	1 -->  "KEYCODE_MENU"
	2 -->  "KEYCODE_SOFT_RIGHT"
	3 -->  "KEYCODE_HOME"
	4 -->  "KEYCODE_BACK"
	5 -->  "KEYCODE_CALL"
	6 -->  "KEYCODE_ENDCALL"
	7 -->  "KEYCODE_0"
	8 -->  "KEYCODE_1"
	9 -->  "KEYCODE_2"
	10 -->  "KEYCODE_3"
	11 -->  "KEYCODE_4"
	12 -->  "KEYCODE_5"
	13 -->  "KEYCODE_6"
	14 -->  "KEYCODE_7"
	15 -->  "KEYCODE_8"
	16 -->  "KEYCODE_9"
	17 -->  "KEYCODE_STAR"
	18 -->  "KEYCODE_POUND"
	19 -->  "KEYCODE_DPAD_UP"
	20 -->  "KEYCODE_DPAD_DOWN"
	21 -->  "KEYCODE_DPAD_LEFT"
	22 -->  "KEYCODE_DPAD_RIGHT"
	23 -->  "KEYCODE_DPAD_CENTER"
	24 -->  "KEYCODE_VOLUME_UP"
	25 -->  "KEYCODE_VOLUME_DOWN"
	26 -->  "KEYCODE_POWER"
	27 -->  "KEYCODE_CAMERA"
	28 -->  "KEYCODE_CLEAR"
	29 -->  "KEYCODE_A"
	30 -->  "KEYCODE_B"
	31 -->  "KEYCODE_C"
	32 -->  "KEYCODE_D"
	33 -->  "KEYCODE_E"
	34 -->  "KEYCODE_F"
	35 -->  "KEYCODE_G"
	36 -->  "KEYCODE_H"
	37 -->  "KEYCODE_I"
	38 -->  "KEYCODE_J"
	39 -->  "KEYCODE_K"
	40 -->  "KEYCODE_L"
	41 -->  "KEYCODE_M"
	42 -->  "KEYCODE_N"
	43 -->  "KEYCODE_O"
	44 -->  "KEYCODE_P"
	45 -->  "KEYCODE_Q"
	46 -->  "KEYCODE_R"
	47 -->  "KEYCODE_S"
	48 -->  "KEYCODE_T"
	49 -->  "KEYCODE_U"
	50 -->  "KEYCODE_V"
	51 -->  "KEYCODE_W"
	52 -->  "KEYCODE_X"
	53 -->  "KEYCODE_Y"
	54 -->  "KEYCODE_Z"
	55 -->  "KEYCODE_COMMA"
	56 -->  "KEYCODE_PERIOD"
	57 -->  "KEYCODE_ALT_LEFT"
	58 -->  "KEYCODE_ALT_RIGHT"
	59 -->  "KEYCODE_SHIFT_LEFT"
	60 -->  "KEYCODE_SHIFT_RIGHT"
	61 -->  "KEYCODE_TAB"
	62 -->  "KEYCODE_SPACE"
	63 -->  "KEYCODE_SYM"
	64 -->  "KEYCODE_EXPLORER"
	65 -->  "KEYCODE_ENVELOPE"
	66 -->  "KEYCODE_ENTER"
	67 -->  "KEYCODE_DEL"
	68 -->  "KEYCODE_GRAVE"
	69 -->  "KEYCODE_MINUS"
	70 -->  "KEYCODE_EQUALS"
	71 -->  "KEYCODE_LEFT_BRACKET"
	72 -->  "KEYCODE_RIGHT_BRACKET"
	73 -->  "KEYCODE_BACKSLASH"
	74 -->  "KEYCODE_SEMICOLON"
	75 -->  "KEYCODE_APOSTROPHE"
	76 -->  "KEYCODE_SLASH"
	77 -->  "KEYCODE_AT"
	78 -->  "KEYCODE_NUM"
	79 -->  "KEYCODE_HEADSETHOOK"
	80 -->  "KEYCODE_FOCUS"
	81 -->  "KEYCODE_PLUS"
	82 -->  "KEYCODE_MENU"
	83 -->  "KEYCODE_NOTIFICATION"
	84 -->  "KEYCODE_SEARCH"
	85 -->  "TAG_LAST_KEYCODE"


### Assert Exists
Make sure if the object exist in the screen.

The usage is similar to "Click" action.
