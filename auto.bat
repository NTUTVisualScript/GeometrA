@ECHO "請以系統管理員身分執行"
@ECHO OFF
pip install Pillow
pip install nose
pip install numpy
pip install opencv-python
setx /m Android_HOME "%USERPROFILE%\AppData\Local\Android\sdk"
setx /m PATH "%PATH%;%Android_HOME%\platform-tools"
PAUSE
