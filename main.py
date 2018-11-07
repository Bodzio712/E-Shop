from flask import *
import sqlite3
import os
import werkzeug

app = Flask(__name__)
app.secret_key = 'ABCD1234'

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/rodzaje")
def rodzaje():
    return render_template('index.html')

@app.route("/producenci")
def producenci():
    return render_template('index.html')


@app.route("/kategorie")
def kategorie():
    return render_template('index.html')

@app.route("/account/profil")
def accountProfil():
    return render_template('index.html')

@app.route("/account/orders")
def accountOrders():
    return render_template('index.html')

@app.route("/cart")
def cart():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port= '8080')