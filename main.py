import flask
import sqlite3
import os
import werkzeug

app = Flask(__name__)
app.secret_key = 'ABCD1234'


if __name__ == '__main__':
    app.run(debug=True)