# Sikuli-Img
Branch from https://github.com/Swind/Sikuli-Img

# 設定開發環境 (Windows)

參考 [Install OpenCV 3 with Python 3 on Windows](https://solarianprogrammer.com/2016/09/17/install-opencv-3-with-python-3-on-windows/)

1. 決定好要使用 x86 會 x64 的版本下載相對應的 Python 3.5.2 [x86](https://www.python.org/ftp/python/3.5.2/python-3.5.2.exe)/[x64](https://www.python.org/ftp/python/3.5.2/python-3.5.2-amd64.exe)

2. 下載 [Microsoft Visual C++ 2015 Redistributable](https://www.microsoft.com/zh-TW/download/details.aspx?id=48145)。也可以直接安裝 [Visual Studio 2015 Community](https://www.visualstudio.com/zh-hans/downloads/)

3. 依照 Python 版本與 x86/x64 下載已經預先編譯好的 [numpy](http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy) 與 [opencv3.1](http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv)

      Python 3.5.2 (x86) 的環境下
      ```
      numpy-1.11.2rc1+mkl-cp35-cp35m-win32.whl
      opencv_python-3.1.0-cp35-cp35m-win32.whl
      ```
      
4. 開啟 cmd 使用 pip 安裝剛剛下載的檔案

      ```bash
      pip install "numpy-1.11.2rc1+mkl-cp35-cp35m-win32.whl"
      pip install "opencv_python-3.1.0-cp35-cp35m-win32.whl"
      ```

5. 測試

      開啟 cmd 執行 pytho

      ```bash
      Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:01:18) [MSC v.1900 32 bit (Intel)] on win32
      Type "help", "copyright", "credits" or "license" for more information.
      >>> import cv2
      >>> print(cv2.__version__)
      3.1.0
      >>> exit()
      ```

# 設定開發環境 (Linux 跟 OSX）

1. Python3
2. OpenCV 3.1.0

可參考 [Install OpenCV 3.0 with Python 3.4 on OSX & Ubuntu](https://github.com/rainyear/lolita/issues/18)

## 安裝 pyenv (為了要讓 Python 不要受系統預設的 Python 環境影響與限制) 與 Python 3.5.2

[pyenv](https://github.com/yyuu/pyenv)

```bash
git clone https://github.com/yyuu/pyenv.git ~/.pyenv

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile

echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
```

安裝 Python 3.5.2

pyenv 會下載 Python 原始碼來編譯，所以要設定參數讓他在編譯的時候順便編譯 shared library

```bash
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.5.2
```

編譯完畢之後下

```bash
ls $HOME/.pyenv/versions/3.5.2/lib
```

應該會看到以下的檔案被編譯出來

```bash
libpython3.5m.so  libpython3.5m.so.1.0  libpython3.so  pkgconfig  python3.5
```

## 編譯 OpenCV3

安裝編譯所需要的 packages

```bash
# Ubuntu
sudo apt-get install build-essential
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
```

```bash

# 下載 OpenCV3
wget https://github.com/opencv/opencv/archive/3.1.0.tar.gz
tar -zxvf 3.1.0.tar.gz
rm 3.1.0.tar.gz

# 下載 OpenCV3-contrib
wget https://github.com/opencv/opencv_contrib/archive/3.1.0.tar.gz
tar -zxvf 3.1.0.tar.gz
rm 3.1.0.tar.gz

# 設定使用 python3 與 python packages
pyenv local 3.5.2
pip install numpy
```

## 使用 cmake 產生 Makefile

進入 `opencv-3.1.0` 

```bash
cd opencv-3.1.0
```

下面可以建立一個 script 檔案，會比較方便執行。
當然也可以直接複製貼上，但是要注意一下下面 `PYTHON_INCLUDE_DIR` 等的路徑是否填寫正確。

```bash
mkdir build
cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.1.0/modules \
      -D BUILD_EXAMPLES=OFF \
      -D INSTALL_C_EXAMPLES=OFF \
      -D PYTHON3_EXECUTABLE=$HOME/.pyenv/shims/python \
      -D PYTHON_INCLUDE_DIR=$HOME/.pyenv/versions/3.5.2/include/python3.5m \
      -D PYTHON_LIBRARY=$HOME/.pyenv/versions/3.5.2/lib/libpython3.5m.so \
      -D ENABLE_PRECOMPILED_HEADERS=OFF \
      ..
```

cmake 產生的訊息中，注意 Python3 這邊是否有正確的找到 Python shared library 的路徑

```
--   Python 3:
--     Interpreter:                 /home/tester/.pyenv/shims/python3 (ver 3.5.2)
--     Libraries:                   /home/swind/.pyenv/versions/3.5.2/lib/libpython3.5m.so (ver 3.5.2)
--     numpy:                       /home/swind/.pyenv/versions/3.5.2/lib/python3.5/site-packages/numpy/core/include (ver 1.11.1)
--     packages path:               lib/python3.5/site-packages
```

## 編譯 OpenCV

```bash
make -j4
make install
```

# 複製 library

在 opencv3.1.0 中的 `build/lib` 資料夾中應該會有 `cv2.cpython-35m-x86_64-linux-gnu.so`

將此檔案複製到 `$HOME/.pyenv/versions/3.5.2/lib/python3.5/cv2.so`

這樣 pyenv 中的 Python 3.5.2 就能找到 cv2 這個 package

```bash
cp lib/python3/cv2.cpython-35m-x86_64-linux-gnu.so /home/tester/.pyenv/versions/3.5.2/lib/python3.5/cv2.so
```

# 測試

```python
import cv2
cv2.__version__
#=> '3.1.0'
```

# 參考連結

[pyenv](https://github.com/yyuu/pyenv)


# Visual Script
Branch from https://github.com/Swind/Sikuli-Img

<<<<<<< HEAD
#使用教學
=======
# 使用教學
>>>>>>> origin/master
[Clone本專案](https://github.com/Yamiyo/Visual_Script.git)

設定系統環境變數

	變數名稱	Android_HOME
	變數值     Android SDK 的安裝路徑
![](/pic/Environmental.PNG)


使用Python 執行 專案中的 src/VisualScript.py

	python D:\VS_project\Visual_Script\src\VisualScript.py

<<<<<<< HEAD
##介面介紹
=======
## 介面介紹
>>>>>>> origin/master
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


<<<<<<< HEAD
##Action動作介紹
###Click
=======
## Action動作介紹
### Click
>>>>>>> origin/master
可從ScreenShot中點選物件，或從Tree View中直接點擊節點
![](/pic/Click.gif)

也可以用拖拉的方式，來尋找物件中的某個畫面
![](/pic/Click2.gif)

<<<<<<< HEAD
###Drag
![](/pic/Drag.gif)

###Input
![](/pic/Input.gif)

###Send Key
=======
### Drag
![](/pic/Drag.gif)

### Input
![](/pic/Input.gif)

### Send Key
>>>>>>> origin/master
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

<<<<<<< HEAD
###Exists
與Click功能用法一樣，是用來驗證該物件的節點路徑是否相同，以及該物件的畫面是否一致
=======
### Exists
與Click功能用法一樣，是用來驗證該物件的節點路徑是否相同，以及該物件的畫面是否一致
>>>>>>> origin/master
