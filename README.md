# Sikuli-Img

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
