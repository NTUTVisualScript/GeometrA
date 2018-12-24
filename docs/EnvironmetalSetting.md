# Environmental Setting

1. [Clone the project](https://github.com/NTUTVisualScript/Visual_Script.git)

2. Install [Python3.6+](https://www.python.org/downloads/)  

3. Install PIL  

    pip3 install -r requirements.txt

7. Installing ADB tool.
  1. Windows OS
    1. Downloads [platform-tools](https://developer.android.com/studio/releases/platform-tools.html)

    2. Set environment variable path  
(Set Android_HOME as the environment variable where you put "platform-tools" directory)
```
    Variable    Path    
    Value       %Android_HOME%\platform-tools  
```
![](/docs/pic/SystemPath.PNG)

  2. Mac OS
```
    brew cask install android-platform-tools
```

  3. Ubuntu
```
    sudo apt install adb
    sudo apt install python3.6-tk  // Or specific for your python version
```

5. Install [Node.js 8+](https://nodejs.org/en/download/current/)
  1. Install **npm 6+** if you don't get one.

6. npm install

7. [Optional] npm install electron -g
