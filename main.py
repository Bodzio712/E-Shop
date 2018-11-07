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
def root():
    return render_template('index.html')

@app.route("/producenci")
def root():
    return render_template('index.html')


@app.route("/kategorie")
def root():
    return render_template('index.html')

@app.route("/account/profil")
def root():
    return render_template('index.html')

@app.route("/account/orders")
def root():
    return render_template('index.html')

@app.route("/account/cart")
def root():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port= '8080')