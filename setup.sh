pip3 install Pillow
pip3 install nose
pip3 install opencv-python
pip3 install flask
pip3 install -U flask-cors

ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install android-platform-tools

read -n 1 -p "Press any key to continue..." INP
if [ $INP != '' ] ; then
        echo -ne '\b \n'
fi
