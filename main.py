# -*- coding: utf-8 -*-
from flask import *
from peewee import *
import sqlite3
import os
import werkzeug
from sqlalchemy import *

app = Flask(__name__)
app.secret_key = 'ABCD1234'

#dane do navbara
engine = create_engine("sqlite:///database.db")
metadata = MetaData()

type = Table('type', metadata, autoload=True, autoload_with=engine)
type_sel = select([type])
manu = Table('manufacturer', metadata, autoload=True, autoload_with=engine)
manu_sel = select([manu])
cats = Table('category', metadata, autoload=True, autoload_with=engine)
cats_sel = select([cats])

typeData = engine.execute(type_sel).fetchall()
manuData = engine.execute(manu_sel).fetchall()
catData = engine.execute(cats_sel).fetchall()


@app.route("/")
def root():
    return render_template('index.html', categoryData=catData, typeData = typeData, manuData = manuData)

@app.route("/rodzaje")
def rodzaje():
    typeId = request.args.get("typeId")
    product = Table('product', metadata, autoload=True, autoload_with=engine)
    prod_sel = select([product]).where(product.c.typeId == typeId)
    prodData = engine.execute(prod_sel).fetchall()
    print(prodData)
    return render_template('index.html', categoryData=catData, typeData = typeData, manuData = manuData, productData = prodData)

@app.route("/producenci")
def producenci():
    producentId = request.args.get("manuId")
    product = Table('product', metadata, autoload=True, autoload_with=engine)
    prod_sel = select([product]).where(product.c.manufacturerId == producentId)
    prodData = engine.execute(prod_sel).fetchall()
    print(prodData)
    return render_template('index.html', categoryData=catData, typeData=typeData, manuData=manuData,
                           productData=prodData)

@app.route("/kategorie")
def kategorie():
    kategoriaId = request.args.get("catId")
    product = Table('product', metadata, autoload=True, autoload_with=engine)
    prod_sel = select([product]).where(product.c.categoryId == kategoriaId)
    prodData = engine.execute(prod_sel).fetchall()
    print(prodData)
    return render_template('index.html', categoryData=catData, typeData=typeData, manuData=manuData,
                           productData=prodData)


@app.route("/account/profil")
def accountProfil():
    return render_template('index.html')


@app.route("/account/orders")
def accountOrders():
    return render_template('index.html')


@app.route("/cart")
def cart():
    return render_template('index.html')


@app.route("/loginForm")
def loginForm():
    return render_template('login.html')


@app.route("/registerForm")
def registerForm():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True, port= '8080')