echo %~dp0
cd %~dp0
set FLASK_APP=src
pip install -e .
flask run