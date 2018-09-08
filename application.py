import os
from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)

app.config["Session_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

data = {}

@app.route('/', methods = ["GET", "POST"])
def index():
    name = request.form.get("item_name")
    price = request.form.get("profit")
    quantity = request.form.get("quantity")
    month = request.form.get("month")
    data[name] = [(price, quantity, month)]
    return render_template("index.html")

@app.route('/details', methods = ["GET", "POST"])
def details():
    return render_template("Details.html", data = data)
if __name__ == '__main__':
    app.debug = True
    app.run()
