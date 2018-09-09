import os
import base64
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, session, send_file
from flask_session import Session
from io import BytesIO
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

@app.route('/image')
def piechart():
    names = []
    profit = []
    plt.figure()
    rows = db.execute("SELECT product_name, quantity, price from product JOIN details on details.details_id =  product.id").fetchall();
    for row in rows:
        names.append(row.product_name)
        profit.append(row.quantity * row.price)
    fig1, ax1 = plt.subplots()
    ax1.pie(profit, labels = names, startangle = 90, autopct = '%1.1f%%')
    ax1.axis('equal')
    img = BytesIO()
    plt.savefig(img, format = 'png')
    img.seek(0)
    return send_file(img, mimetype = 'image/png')

@app.route('/image1')
def bargraph():
    names = []
    profit = []
    plt.figure()
    rows = db.execute("SELECT product_name, quantity from product JOIN details on details.details_id =  product.id").fetchall();
    for row in rows:
        names.append(row.product_name)
        profit.append(row.quantity)
    plt.barh(names, profit)
    img1 = BytesIO()
    plt.savefig(img1, format = 'png')
    img1.seek(0)
    return send_file(img1, mimetype = 'image/png')

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8080)
