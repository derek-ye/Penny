import flask
from receipt import ocr_space_file as ocr
"""
ocr(filename) --> json with contents
"""

app = flask.Flask(__name__)

@app.route('/about')
def about():
    return "made by snacc overflow 3.0"

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/index.html')
def indexNav():
    return flask.render_template('index.html')

@app.route('/generic.html')
def registerNav():
    return flask.render_template('generic.html')

@app.route('/master.html')
def loginNav():
    return flask.render_template('master.html')

if __name__ == '__main__':
    app.run(debug=True)