echo %~dp0
cd %~dp0
set FLASK_APP=VisualScript
pip install -e .
flask run
