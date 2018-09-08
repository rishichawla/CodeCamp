import os
from flask import Flask, render_template, request, session
from flask_session import Session

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

app.config["Session_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine('postgresql://postgres:admin@localhost/salesanalysis')
db = scoped_session(sessionmaker(bind = engine))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/feed', methods = ["POST"])
def details():
    product_name = request.form.get("product_name")
    price = request.form.get("price")
    db.execute("INSERT into product (product_name, price) VALUES (:product_name, :price)", {"product_name": product_name, "price": price})
    db.commit()
    print(f"Succesfully added {{product_name}} that costs {{price}}")
    details = db.execute("SELECT id from product where product_name = :product_name",{"product_name": product_name}).fetchone();
    details_id = int(details.id)
    month = request.form.get("month")
    quantity = request.form.get("quantity")
    db.execute("INSERT into details (month, quantity, details_id) VALUES (:month, :quantity, :details_id)", {"month": month, "quantity": quantity, "details_id": details_id})
    db.commit()
    print(f"Succesfully updated {{month}} that costs {{quantity}}")
    return render_template("index.html")

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8080)
