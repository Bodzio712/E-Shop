# -*- coding: utf-8 -*-
from flask import *
from peewee import *
import sqlite3
import os
import werkzeug
from sqlalchemy import *
from sqlalchemy.orm import *


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
    return render_template('index.html', categoryData=catData, typeData = typeData, manuData = manuData,
                           productData = prodData)

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
    return render_template('index.html', categoryData=catData, typeData=typeData, manuData=manuData,
                           productData=prodData)

@app.route("/addToCart")
def addToCart():
        productId = int(request.args.get('productId'))
        clientId = 99
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
  #          cur.execute("SELECT userId FROM users WHERE email = '" + session['email'] + "'")
  #          userId = cur.fetchone()[0]
  #          try:
            cur.execute("INSERT INTO cart (clientId, productId) VALUES (?, ?)", (clientId, productId))
            conn.commit()
#                msg = "Added successfully"
#            except:
#                conn.rollback()
#                msg = "Error occured"
        conn.close()
        return redirect(url_for('root'))

@app.route("/cart")
def cart():
#    if 'email' not in session:
#        return redirect(url_for('loginForm'))
#    loggedIn, firstName, noOfItems = getLoginDetails()
#    email = session['email']
    product = Table('product', metadata, autoload=True, autoload_with=engine)
    cart = Table('cart', metadata, autoload=True, autoload_with=engine)
    meta = select([product, cart], product.c.productId == cart.c.productId)
    cp_data = engine.execute(meta).fetchall()
    return render_template("index.html", categoryData=catData, typeData=typeData, manuData=manuData,
                           products=cp_data)



@app.route("/account/profil")
def accountProfil():
    return render_template('index.html')

@app.route("/account/orders")
def accountOrders():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port= '8080')