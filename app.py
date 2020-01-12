import flask
import pickle as pkl
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

@app.route('/master.html', methods = ['GET', 'POST'])
def loginNav():
    
    return flask.render_template('master.html')

@app.route('/blank.html')
def budgetNav():
    try:
        budget = pkl.load(open("budget.pkl", "rb" ))
    except FileNotFoundError:
        budget = 0
    budget = '${:,.2f}'.format(budget)
    return flask.render_template('blank.html', budget=budget)

@app.route('/blank.html', methods = ['GET', 'POST'])
def budgetNav_post():
    budget = flask.request.form['budget']
    budget = float(budget)
    pkl.dump(budget, open("budget.pkl", "wb"))
    budget = '${:,.2f}'.format(budget)
    return flask.render_template('blank.html', budget=budget)

@app.route('/tables.html')
def tableNav():
    return flask.render_template('tables.html')
    

if __name__ == '__main__':
    app.run(debug=True)