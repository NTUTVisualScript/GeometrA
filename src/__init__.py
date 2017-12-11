from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from src import View
