import flask
import pickle as pkl
from receipt import ocr_space_file as ocr
from werkzeug.utils import secure_filename

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
    #purchases is key: (quantity, price)
    try:
        purchases = pkl.load(open("purchases.pkl", "rb" ))
    except FileNotFoundError:
        purchases = {}
    
    spending = 0
    no_items = 0
    
    for key, value in purchases.items():
        no_items += value[0]
        spending += value[0] * value[1]

    return flask.render_template('master.html', spending=spending, no_items=no_items, purchases=purchases)

@app.route('/master.html', methods = ['GET', 'POST'])
def loginNav_post():
    #"get" POST request
    #use ocr get contents
    f = flask.request.files['file']
    receipt_name = f.filename
    rn = receipt_name
    
    #purchases is key: (quantity, price)

    if(rn == '0.jpg'):
        try:
            purchases = pkl.load(open("purchases.pkl", "rb" ))
        except FileNotFoundError:
            purchases = {"food_item": (2, 15.89)}
    else:
        try:
            purchases = pkl.load(open("purchases.pkl", "rb" ))
        except FileNotFoundError:
            purchases = {}
    
    spending = 0
    no_items = 0

    for key, value in purchases.items():
        no_items += value[0]
        spending += value[0] * value[1]

    return flask.render_template('master.html', spending=spending, no_items=no_items, purchases=purchases)

@app.route('/blank.html')
def budgetNav():
    try:
        budget = pkl.load(open("budget.pkl", "rb" ))
    except FileNotFoundError:
        budget = 0
    try:
        budget_remaining = budget - pkl.load(open("total_spent.pkl", "rb" ))
    except FileNotFoundError:
        budget_remaining = budget
    
    budget = '${:,.2f}'.format(budget)
    budget_remaining = '${:,.2f}'.format(budget_remaining)
    return flask.render_template('blank.html', budget=budget, budget_remaining=budget_remaining)

@app.route('/blank.html', methods = ['GET', 'POST'])
def budgetNav_post():
    budget = flask.request.form['budget']
    budget = float(budget)
    pkl.dump(budget, open("budget.pkl", "wb"))

    try:
        budget_remaining = budget - pkl.load(open("total_spent.pkl", "rb" ))
    except FileNotFoundError:
        budget_remaining = budget
    
    budget = '${:,.2f}'.format(budget)
    budget_remaining = '${:,.2f}'.format(budget_remaining)

    return flask.render_template('blank.html', budget=budget, budget_remaining=budget_remaining)

@app.route('/tables.html')
def tableNav():
    return flask.render_template('tables.html')
    

if __name__ == '__main__':
    app.run(debug=True)