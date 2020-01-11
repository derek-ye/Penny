import flask

app = flask.Flask(__name__)

@app.route('/about')
def about():
    return "made by snacc overflow 3.0"

@app.route('/')
def index():
    """ Page at '/' """
    # no 'templates/' before file -> Flask auto checks 'templates' folder
    return flask.render_template('index.html')

@app.route('/generic.html')
def generic():
    """ Page at '/' """
    # no 'templates/' before file -> Flask auto checks 'templates' folder
    return flask.render_template('generic.html')

@app.route('/master.html')
def master():
    """ Page at '/' """
    # no 'templates/' before file -> Flask auto checks 'templates' folder
    return flask.render_template('master.html')


if __name__ == '__main__':
    app.run(debug=True)