# Visual Script
Branch from https://github.com/Swind/Sikuli-Img

# 開啟方法

1.完成下方[環境建置] 或 以系統管理員身份執行 'auto.bat'
2.執行根目錄下 'run.bat'
3.打開browser，連線到 "http://127.0.0.1:5000"

# 環境建置

1.[Clone本專案](https://github.com/NTUTVisualScript/Visual_Script.git)

2.Install [Python3](https://www.python.org/downloads/)  

    Check: "The version SHOULD BE **3** !!"

3.Install [Android Studio](https://developer.android.com/studio/index.html)  

4.請以*系統管理員身分執行專案根目錄下的 auto.bat*
  或是*執行以下的環境設定*

# 環境設定

1.Install PIL  

    pip install Pillow

2.Install opencv3  

    pip install opencv_python

3.Install numpy  

    pip install numpy  

4.Set environment variable  

    Variable    Android_HOME    
    Value   Android SDK 的安裝路徑  

![](/pic/Environmental.PNG)

5.Set environment variable path  

    Variable    Path    
    Value   %Android_HOME%\platform-tools  

![](/pic/SystemPath.PNG)

6.Install Flask

    pip install flask

7.Install flask-cors

    pip install -U flask-cors


# 使用教學
使用Python 執行 專案中的 src/VisualScript.py  

    python D:\VS_project\Visual_Script\src\VisualScript.py

## 介面介紹

![](/pic/View_Introduction.png)

	================================
	Dump UI Button 會對手機下達ADB指令
	1. adb shell screencap
	2. adb shell uiautomator dump

	將screencap的圖片顯示在Screenshot View中
	將dump下來的XML檔解讀顯示在Tree View中
	================================
	+ Button
	在此插入一行
	================================
	- Button
	刪除這一行
	================================
	▶ Button
	執行單一這行
	================================
	Run Button
	執行TestCase View中的腳本
	================================
	Reset TestCase Button
	重置TestCase Virw中的所有動作
	================================
	Action Combobox
	動作選擇
	================================
	Values Text
	根據動作自動或被動地填入內容



## Action動作介紹
### Click

可從ScreenShot中點選物件，或從Tree View中直接點擊節點
![](/pic/Click.gif)

也可以用拖拉的方式，來尋找物件中的某個畫面
![](/pic/Click2.gif)


### Drag
![](/pic/Drag.gif)

### Input
![](/pic/Input.gif)

### Send Key

![](/pic/Send_key.gif)

可根據自行想使用的ADB keycode來自行輸入
keycode指令請參考

[Keycode 列表](http://blog.csdn.net/jlminghui/article/details/39268419)

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


### Exists
與Click功能用法一樣，是用來驗證該物件的節點路徑是否相同，以及該物件的畫面是否一致
