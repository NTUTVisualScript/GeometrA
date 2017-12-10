from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/VisualScript')
def html():
    return render_template('index.html', mylist=[1, 2, 3, 4, 5])


if __name__ == '__main__':
    app.run()
