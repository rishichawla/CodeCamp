import os
from flask import Flask, render_template, request, session
from flask_session import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

app.config["Session_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind = engine))

@app.route('/', methods = ["GET", "POST"])
def index():
    return render_template("index.html")

@app.route('/details', methods = ["GET", "POST"])
def details():
    months = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]
    return render_template("Details.html", months = months)
if __name__ == '__main__':
    app.debug = True
    app.run()
