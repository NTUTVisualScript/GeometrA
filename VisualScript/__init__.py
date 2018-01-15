from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/VisualScript')
def html():
    return render_template('index.html')

from VisualScript.router import WorkSpaceRouter
