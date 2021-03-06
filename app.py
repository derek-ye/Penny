import flask
import pickle as pkl
from receipt import ocr_space_file as ocr
from werkzeug.utils import secure_filename
import json
import os

os.system("rm *.pkl")
os.system("rm static/*.txt")
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
    pkl.dump(spending, open("spending.pkl", "wb"))
    ftxt = open("static/spending.txt","w+")
    ftxt.write(str(spending))
    ftxt.close()
    spending = '${:,.2f}'.format(spending)
    try:
        budget = pkl.load(open("budget.pkl", "rb" ))
    except FileNotFoundError:
        budget = 0
    budget = '${:,.2f}'.format(budget)

    categories = {'food': "0", 'electronics': "0"}
    for key, value in purchases.items():
        categories[value[2]] = str(int(categories[value[2]]) + value[0])

    js_value = json.dumps(categories)
    #print(js_value)

    return flask.render_template('master.html', spending=spending, budget=budget, no_items=no_items, purchases=purchases, purch=js_value)

@app.route('/master.html', methods = ['GET', 'POST'])
def loginNav_post():
    #"get" POST request
    #use ocr get contents
    f = flask.request.files['file']
    receipt_name = f.filename
    rn = receipt_name
    
    #purchases is key: (quantity, price)

    if(rn == '0.png'):
        try:
            purchases = pkl.load(open("purchases.pkl", "rb" ))
            if("eggs" in purchases):
                purchases["eggs"][0] += 1
            else:
                purchases["eggs"] = [1, 5.20, 'food']
            if("milk" in purchases):
                purchases["milk"][0] += 2
            else:
                purchases["milk"] = [2, 5.99, 'food']
        except FileNotFoundError:
            purchases = {"eggs": [1, 5.20, 'food'], "milk": [2, 5.99, 'food']}
    elif(rn == '1.png'):
        try:
            purchases = pkl.load(open("purchases.pkl", "rb" ))
            if("switch" in purchases):
                purchases["switch"][0] += 1
            else:
                purchases["switch"] = [1, 249.99, 'electronics']
            if("smash" in purchases):
                purchases["smash"][0] += 1
            else:
                purchases["smash"] = [1, 59.99, 'electronics']
            if("hersheys" in purchases):
                purchases["hersheys"][0] += 1
            else:
                purchases["hersheys"] = [1, 1.99, 'food']
        except FileNotFoundError:
            purchases = {"switch": [1, 249.99, 'electronics'], "smash": [1, 59.99, 'electronics'], "hersheys": [1, 1.99, 'food']}
    elif(rn == "2.png"):
        try:
            purchases = pkl.load(open("purchases.pkl", "rb" ))
            if("peanut butter" in purchases):
                purchases["peanut butter"][0] += 1
            else:
                purchases["peanut butter"] = [1, 3.50, 'food']
            if("light bulbs" in purchases):
                purchases["light bulbs"][0] += 1
            else:
                purchases["light bulbs"] = [1, 14.99, 'electronics']
        
        except FileNotFoundError:
            purchases = {"peanut butter": [1, 3.50, 'food'], "light bulbs": [1, 14.99, 'electronics']}
    else:
        try:
            purchases = pkl.load(open("purchases.pkl", "rb" ))
        except FileNotFoundError:
            purchases = {}
    
    pkl.dump(purchases, open("purchases.pkl", "wb"))
    ftxt = open("static/purchases.txt","w+")
    for key, value in purchases.items():
        ftxt.write(str(key) + " " + str(value[2]))
    ftxt.close()
    
    spending = 0
    no_items = 0

    for key, value in purchases.items():
        no_items += value[0]
        spending += value[0] * value[1]
    pkl.dump(spending, open("spending.pkl", "wb"))
    ftxt = open("static/spending.txt","w+")
    ftxt.write(str(spending))
    ftxt.close()
    spending = '${:,.2f}'.format(spending)

    try:
        budget = pkl.load(open("budget.pkl", "rb" ))
    except FileNotFoundError:
        budget = 0
    budget = '${:,.2f}'.format(budget)

    categories = {'food': "0", 'electronics': "0"}
    for key, value in purchases.items():
        categories[value[2]] = str(int(categories[value[2]]) + value[0])

    js_value = json.dumps(categories)
    #print(js_value)

    return flask.render_template('master.html', spending=spending, budget=budget, no_items=no_items, purchases=purchases, purch=js_value)

@app.route('/blank.html')
def budgetNav():
    try:
        budget = pkl.load(open("budget.pkl", "rb" ))
    except FileNotFoundError:
        budget = 0
    try:
        budget_remaining = budget - pkl.load(open("spending.pkl", "rb" ))
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
        budget_remaining = budget - pkl.load(open("spending.pkl", "rb" ))
    except FileNotFoundError:
        budget_remaining = budget
    
    budget = '${:,.2f}'.format(budget)
    budget_remaining = '${:,.2f}'.format(budget_remaining)

    return flask.render_template('blank.html', budget=budget, budget_remaining=budget_remaining)

@app.route('/tables.html')
def tableNav():
    #purchases is key: (quantity, price)
    try:
        purchases = pkl.load(open("purchases.pkl", "rb" ))
    except FileNotFoundError:
        purchases = {}
    return flask.render_template('tables.html', purchases=purchases)
    

if __name__ == '__main__':
    app.run(debug=True)