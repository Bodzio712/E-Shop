# -*- coding: utf-8 -*-
from flask import *
from peewee import *
import sqlite3
from sqlalchemy.orm import *
import os
import werkzeug
from sqlalchemy import *
from sqlalchemy.ext.automap import *
from sqlalchemy.pool import StaticPool

app = Flask(__name__)
app.secret_key = 'ABCD1234'

#dane do navbara
engine = create_engine("sqlite:///database.db",
                    connect_args={'check_same_thread':False},
                    poolclass=StaticPool)
metadata = MetaData(engine, reflect=True)

def xyz():
 con = engine.connect()
 type = metadata.tables['type']
 manu = metadata.tables['manufacturer']
 cats = metadata.tables['category']
 product = metadata.tables['product']
 cart = metadata.tables['cart']

 type_sel = select([type])
 manu_sel = select([manu])
 cats_sel = select([cats])
 product_sel = select([product])
 cart_sel = select([cart])

 typeData = con.execute(type_sel).fetchall()
 manuData = con.execute(manu_sel).fetchall()
 catData = con.execute(cats_sel).fetchall()
 productData = con.execute(product_sel).fetchall()
 cartData = con.execute(cart_sel)

 con.close()
 return typeData, manuData, catData

xyz()

def item_number():
    con = engine.connect()
    noOfItems = con.execute("SELECT count(productId) FROM cart").fetchone()[0]
    #engine.dispose()
    con.close()
    return noOfItems

@app.route("/")
def root():
    item_no = item_number()
    con = engine.connect()
    product = metadata.tables['product']
    meta = select([product])
    products = con.execute(meta)
    con.close()
    typeData, manuData, catData = xyz()
    return render_template('index.html', categoryData=catData, typeData = typeData, manuData = manuData, noOfItems=item_no, productData=products)

@app.route("/rodzaje")
def rodzaje():
    con = engine.connect()
    typeId = request.args.get("typeId")
    product = Table('product', metadata, autoload=True, autoload_with=engine)
    prod_sel = select([product]).where(product.c.typeId == typeId)

    prodData = con.execute(prod_sel).fetchall()
    print(prodData)
    #x = json.dumps([dict(r) for r in prodData])
    #print(x)
    #engine.dispose()
    con.close()
    typeData, manuData, catData = xyz()
    return render_template('index.html', categoryData=catData, typeData = typeData, manuData = manuData, productData = prodData)

@app.route("/producenci")
def producenci():
    con = engine.connect()
    producentId = request.args.get("manuId")
    product = Table('product', metadata, autoload=True, autoload_with=engine)
    prod_sel = select([product]).where(product.c.manufacturerId == producentId)
    prodData = engine.execute(prod_sel).fetchall()
    print(prodData)
    #engine.dispose()
    con.close()
    typeData, manuData, catData = xyz()
    return render_template('index.html', categoryData=catData, typeData=typeData, manuData=manuData,
                           productData=prodData)

@app.route("/kategorie")
def kategorie():
    con = engine.connect()
    kategoriaId = request.args.get("catId")
    product = Table('product', metadata, autoload=True, autoload_with=engine)
    prod_sel = select([product]).where(product.c.categoryId == kategoriaId)
    prodData = engine.execute(prod_sel).fetchall()
    print(prodData)
    #engine.dispose()
    con.close()
    typeData, manuData, catData = xyz()
    return render_template('index.html', categoryData=catData, typeData=typeData, manuData=manuData,
                           productData=prodData)

@app.route("/addToCart", methods=["GET", "POST"])
def addToCart():
        for key, value in request.form.items():
            print("key: {0}, value: {1}".format(key, value))
        print("QUANTITY:")
        quant = request.form['liczba']
        print(quant)
        con = engine.connect()
        productId = int(request.args.get('productId'))
        clientId = 99
        cart = metadata.tables['cart']
        ins2 = cart.insert().values(clientId = clientId, productId=productId, quantity=quant)
        x = con.execute(ins2)
        #engine.dispose()
        con.close()
        return redirect(url_for('root'))
        # commit the record the database

#        with sqlite3.connect('database.db') as conn:
#            cur = conn.cursor()
  #          cur.execute("SELECT userId FROM users WHERE email = '" + session['email'] + "'")
  #          userId = cur.fetchone()[0]
  #          try:
#            cur.execute("INSERT INTO cart (clientId, productId) VALUES (?, ?)", (clientId, productId))
#            conn.commit()
#                msg = "Added successfully"
#            except:
#                conn.rollback()
#                msg = "Error occured"
#        conn.close()


@app.route("/cart")
def cart():
#    if 'email' not in session:
#        return redirect(url_for('loginForm'))
#    loggedIn, firstName, noOfItems = getLoginDetails()
#    email = session['email']
    con = engine.connect()
    product = metadata.tables['product']
    cart = metadata.tables['cart']
    meta = select([product, cart], cart.c.productId == product.c.productId)
    cp_data = con.execute(meta).fetchall()
    #engine.dispose()
    con.close()

    catData, typeData, manuData = xyz()
    return render_template("index.html", categoryData=catData, typeData=typeData, manuData=manuData,
                           products=cp_data)

def delete_cart():
 con = engine.connect()
 d = delete(cart)
 con.execute(d)
 engine.dispose()
 con.close()
@app.route("/placeOrder")
def placeOrder():

  with engine.connect() as connection:
    product = metadata.tables['product']
    cart = metadata.tables['cart']
    orders = metadata.tables['orders']

    join_obj = product.join(cart, product.c.productId == cart.c.productId)
    join_sel = select([product.c.productId, product.c.productName]).select_from(join_obj)#select statement
    prod_data = connection.execute(join_sel)#fetch data
    #stworz tabele orders i zapisz do bazy\

    for row in prod_data:
        ins = orders.insert().values(
        productId=row.productId,
        productName=row.productName,
        categoryId=1,
        clientId=11,
        clientAddress='adress',
        idNip=21,
        deliveryId=21,
        paymentId=21,
        date='21.10.2018',
        quantity=10,
        valueNet=99.9,
        valueGross=77.8)
        connection.execute(ins)
  connection.close()

  cond = engine.connect()
  d = delete(cart)
  cond.execute(d)
  engine.dispose()
  cond.close()
  return render_template("index.html")


@app.route("/removeCart")
def removeFromCart():
    con = engine.connect()
    removeId = request.args.get("productId")
    cart = metadata.tables['cart']
    d = delete(cart, cart.c.productId == removeId)
    con.execute(d)
    #engine.dispose()
    con.close()
    return redirect(url_for('cart'))

@app.route("/tmp")
def cart2():
#    if 'email' not in session:
#        return redirect(url_for('loginForm'))
#    loggedIn, firstName, noOfItems = getLoginDetails()
#    email = session['email']
    con = engine.connect()
    product = Table('product', metadata, autoload=True, autoload_with=engine)
    cart = Table('cart', metadata, autoload=True, autoload_with=engine)
    meta = select([product, cart], product.c.productId == cart.c.productId)
    cp_data = con.execute(meta).fetchall()
    con.close()
    catData, typeData, manuData = xyz()
    return render_template("index.html", categoryData=catData, typeData=typeData, manuData=manuData,
                           products=cp_data)

@app.route("/account/profil")
def accountProfil():
    return render_template('index.html')


@app.route("/account/orders")
def accountOrders():
    con = engine.connect()
    orders = metadata.tables['orders']
    ord_sel = select([orders])

    productData = con.execute(ord_sel).fetchall()
    for row in productData:
        print(row)
    #engine.dispose()
    con.close()
    return render_template("index.html", orders=productData)



@app.route("/registerForm", methods = ['GET', 'POST'])
def registerForm():
    return render_template('register.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
            if request.method == 'POST':
                # Parse form data
                password = request.form['password']
                email = request.form['email']
                firstName = request.form['firstName']
                lastName = request.form['lastName']
                address = request.form['address']
                tel = request.form['phone']

                con = engine.connect()
                client = metadata.tables['client']
                client_insert = client.insert().values(
                    firstName=firstName,
                    lastName=lastName,
                    clientAddress=address,
                    email=email,
                    phone=tel,
                    deliveryId = 1,
                    paymentId = 1)
                save = con.execute(client_insert)
                con.close()
            return render_template("index.html")
@app.route("/loginForm")
def loginForm():
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('root'))

if __name__ == '__main__':
    app.run(debug=True, port= '8080')
    #engine.dispose()