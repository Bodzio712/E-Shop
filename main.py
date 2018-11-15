# -*- coding: utf-8 -*-
from flask import *
from peewee import *
import logging
import sqlite3
from sqlalchemy.orm import *
import os
import werkzeug
from sqlalchemy import *
from sqlalchemy.ext.automap import *
from sqlalchemy.pool import StaticPool
import hashlib
import datetime
import json

app = Flask(__name__)
app.secret_key = 'ABCD1234'
logger = logging.getLogger('ftpuploader')
logging.getLogger('sqlalchemy')
logging.getLogger('flask')
hdlr = logging.FileHandler('ftplog.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
FTPADDR = "/"

#dane do navbara
engine = create_engine("sqlite:///database.db",
                    connect_args={'check_same_thread':False},
                    poolclass=StaticPool)
metadata = MetaData(engine, reflect=True)

def xyz():
    con = engine.connect()
    try:
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
        cartData = con.execute(cart_sel).fetchall()

    except Exception as e:
        con.close()
        logger.error('Failed to upload to ftp: ' + str(e) + " Username: " + "TEST" + " URL: " + url_for('root'))
     #otworz contabele
     #dodaj do tabelki
     #zamknij conn
    con.close()
    return (typeData, manuData, catData)

def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            cur.execute("SELECT clientId, firstName FROM client WHERE email = '" + session['email'] + "'")
            userId, firstName = cur.fetchone()
    conn.close()
    return (loggedIn, firstName)

def item_number():
    con = engine.connect()
    try:
        noOfItems = con.execute("SELECT count(productId) FROM cart").fetchone()[0]
    except Exception as e:
        con.close()
        logger.error('Failed to upload to ftp: ' + str(e) + " Username: " + "TEST" + " URL: " + request.base_url )
    con.close()
    return noOfItems

@app.route("/", methods=['POST', 'GET'])
def root():
    loggedIn, firstName= getLoginDetails()
    typeData, manuData, catData = xyz()
    item_no = item_number()
    con = engine.connect()
    try:
        product = metadata.tables['product']
        manufacturer = metadata.tables['manufacturer']
        join_prod_man = product.join(manufacturer, product.c.manufacturerId == manufacturer.c.manufacturerId)
        join_sel = select([product.c.productName, product.c.productId, product.c.description, product.c.priceGross, product.c.manufacturerId, manufacturer.c.name]).select_from(join_prod_man)
        products = con.execute(join_sel).fetchall()
    except Exception as e:
        con.close()
        logger.error('Failed to upload to ftp: ' + str(e) + " Username: " + firstName + " URL: " + request.base_url)
    con.close()
    typeData, manuData, catData = xyz()
    return render_template('index.html', categoryData=catData, typeData = typeData, manuData = manuData, noOfItems=item_no, productData=products, loggedIn = loggedIn)
    #return render_template('index.html', xa = xa)

@app.route("/example", methods=['POST', 'GET'])
def example():
    con = engine.connect()
    try:
        product = metadata.tables['product']
        manufacturer = metadata.tables['manufacturer']
        join_prod_man = product.join(manufacturer, product.c.manufacturerId == manufacturer.c.manufacturerId)
        join_sel = select([product.c.productName, product.c.productId, product.c.description, product.c.priceGross, product.c.manufacturerId, manufacturer.c.name]).select_from(join_prod_man)
        products = con.execute(join_sel).fetchall()
    except Exception as e:
        con.close()
        logger.error('Failed to upload to ftp: ' + str(e) + " Username: " + firstName + " URL: " + request.base_url)
    con.close()
    xa = json.dumps([dict(r) for r in products])
    return jsonify(xa)



@app.route("/rodzaje")
def rodzaje():
    loggedIn, firstName= getLoginDetails()
    typeData, manuData, catData = xyz()
    item_no = item_number()
    con = engine.connect()
    try:
        typeId = request.args.get("typeId")
        product = Table('product', metadata, autoload=True, autoload_with=engine)
        manufacturer = metadata.tables['manufacturer']
        join_prod_man = product.join(manufacturer, product.c.manufacturerId == manufacturer.c.manufacturerId)
        join_sel = select([product.c.productName, product.c.productId, product.c.description, product.c.priceGross, product.c.manufacturerId, manufacturer.c.name]).select_from(join_prod_man).where(product.c.typeId == typeId)
        prodData = con.execute(join_sel).fetchall()
    except Exception as e:
        con.close()
        logger.error('Failed to upload to ftp: ' + str(e) + " Username: " + firstName + " URL: " + request.base_url)
    con.close()
    return render_template('index.html', categoryData=catData, typeData = typeData, manuData = manuData, noOfItems=item_no, productData = prodData, loggedIn = loggedIn)

@app.route("/producenci")
def producenci():
    loggedIn, firstName= getLoginDetails()
    typeData, manuData, catData = xyz()
    item_no = item_number()
    con = engine.connect()
    try:
        producentId = request.args.get("manuId")
        product = Table('product', metadata, autoload=True, autoload_with=engine)
        manufacturer = metadata.tables['manufacturer']
        join_prod_man = product.join(manufacturer, product.c.manufacturerId == manufacturer.c.manufacturerId)
        join_sel = select([product.c.productName, product.c.productId, product.c.description, product.c.priceGross, product.c.manufacturerId, manufacturer.c.name]).select_from(join_prod_man).where(product.c.manufacturerId == producentId)
        prodData = con.execute(join_sel).fetchall()
    except Exception as e:
        con.close()
        logger.error('Failed to upload to ftp: ' + str(e) + " Username: " + firstName + " URL: " + request.base_url)
    con.close()

    return render_template('index.html', categoryData=catData, typeData=typeData, manuData=manuData, noOfItems=item_no, productData=prodData, loggedIn = loggedIn)

@app.route("/kategorie")
def kategorie():
    loggedIn, firstName= getLoginDetails()
    typeData, manuData, catData = xyz()
    item_no = item_number()
    con = engine.connect()
    try:
        kategoriaId = request.args.get("catId")
        product = Table('product', metadata, autoload=True, autoload_with=engine)
        manufacturer = metadata.tables['manufacturer']
        join_prod_man = product.join(manufacturer, product.c.manufacturerId == manufacturer.c.manufacturerId)
        join_sel = select([product.c.productName, product.c.productId, product.c.description, product.c.priceGross, product.c.manufacturerId, manufacturer.c.name]).select_from(join_prod_man).where(product.c.categoryId == kategoriaId)
        prodData = con.execute(join_sel).fetchall()
    except Exception as e:
        con.close()
        logger.error('Failed to upload to ftp: ' + str(e) + " Username: " + firstName + " URL: " + request.base_url)
    con.close()
    return render_template('index.html', categoryData=catData, typeData=typeData, manuData=manuData, noOfItems=item_no, productData=prodData, loggedIn = loggedIn)

@app.route("/addToCart", methods=["GET", "POST"])
def addToCart():
        loggedIn, firstName = getLoginDetails()
        for key, value in request.form.items():
            print("key: {0}, value: {1}".format(key, value))
        print("QUANTITY:")
        quant = request.form['liczba']
        typeData, manuData, catData = xyz()
        item_no = item_number()
        con = engine.connect()
        try:
            con = engine.connect()
            productId = int(request.args.get('productId'))
            clientId = 99
            cart = metadata.tables['cart']
            ins2 = cart.insert().values(clientId = clientId, productId=productId, quantity=quant)
            x = con.execute(ins2)

        except Exception as e:
            con.close()
            logger.error('Failed to upload to ftp: ' + str(e) + " Username: " + firstName + " URL: " + request.base_url)
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
    loggedIn, firstName= getLoginDetails()
    loggedIn = "YES"
    typeData, manuData, catData = xyz()
    item_no = item_number()

    if 'email' not in session:
        return redirect(url_for('loginForm'))
    email = session['email']

    con = engine.connect()
    try:
        product = metadata.tables['product']
        cart = metadata.tables['cart']
        delivery = metadata.tables['delivery']
        payment = metadata.tables['payment']
        meta = select([product, cart], cart.c.productId == product.c.productId)
        #join = cart.join(product, product.c.productId == cart.c.productId)
        #meta = select([cart.c.cartId, cart.c.productId, product.c.categoryId, product.c.productName]).select_from(join)
        #cp_data = engine.execute(meta).fetchall()
        join_obj = cart.join(product, product.c.productId == cart.c.productId)
        join_sel = select([product.c.productId, product.c.productName, product.c.manufacturerId, cart.c.cartId, cart.c.quantity, product.c.priceNet, product.c.priceGross]).select_from(join_obj)#select statement
        cp_data = con.execute(join_sel).fetchall()#fetch data

        # Pobieranie z bazy danych o metodach dostawy
        select_delivery = select([delivery])
        delivery_data = con.execute(select_delivery).fetchall()

        # Pobieranie z bazy danych o metodach płatności
        select_payment = select([payment])
        paymant_data = con.execute(select_payment).fetchall()


    except Exception as e:
        con.close()
        logger.error('Failed to upload to ftp: ' + str(e) + " Username: " + firstName + " URL: " + request.base_url)
    con.close()
    return render_template("index.html", categoryData=catData, typeData=typeData, manuData=manuData, noOfItems=item_no, products=cp_data, loggedIn = loggedIn, deliveryData=delivery_data, paymentData=paymant_data)

def delete_cart():
    loggedIn, firstName= getLoginDetails()
    try:
        con = engine.connect()
        cart = metadata.tables['cart']
        d = delete(cart)
        con.execute(d)
    except Exception as e:
        con.close()
        logger.error('Failed to upload to ftp: ' + str(e) + " Username: " + firstName + " URL: " + request.base_url)
    con.close()

@app.route("/placeOrder", methods=["POST"])
def placeOrder():
  loggedIn, firstName = getLoginDetails()
  with engine.connect() as connection:
    try:
        # email klienta pobierany z cookie
        email = session['email']

        delivery = metadata.tables['delivery']
        payment = metadata.tables['payment']
        client = metadata.tables['client']

        product = metadata.tables['product']
        cart = metadata.tables['cart']
        orders = metadata.tables['orders']

        join_obj = product.join(cart, product.c.productId == cart.c.productId)
        join_sel = select([product.c.productId, product.c.productName, product.c.categoryId, cart.c.quantity]).select_from(join_obj)#select statement
        prod_data = connection.execute(join_sel)#fetch data

        # Pobieranie z bazy danych o metodach dostawy
        select_delivery = select([delivery])
        delivery_data = connection.execute(select_delivery).fetchall()

        # Pobieranie z bazy danych o metodach płatności
        select_payment = select([payment])
        paymant_data = connection.execute(select_payment).fetchall()

        select_clientId = select([client]).where(client.c.email == email)
        client_data = connection.execute(select_clientId).fetchall()

        for row in client_data:
            clientId = row.clientId
            clientAdress = row.clientAddress

        #stworz tabele orders i zapisz do bazy

        for row in prod_data:
            ins = orders.insert().values(
            productId=row.productId,
            productName=row.productName,
            categoryId=row.categoryId,
            clientId=clientId,
            clientAddress=clientAdress,
            idNip=1,
            deliveryId=request.form['delivery-collection'],
            paymentId=request.form['payment-collection'],
            date=datetime.date.today(),
            quantity=row.quantity,
            valueNet=99.9,
            valueGross=77.8)
            connection.execute(ins)
    except Exception as e:
        connection.close()
        logger.error('Failed to upload to ftp: ' + str(e) + " Username: " + firstName + " URL: " + request.base_url)
    connection.close()

  delete_cart()
  return redirect(url_for('root'))


@app.route("/removeCart")
def removeFromCart():
    loggedIn, firstName= getLoginDetails()
    con = engine.connect()
    try:
        removeId = request.args.get("cartId")
        cart = metadata.tables['cart']
        d = delete(cart, cart.c.cartId == removeId, )
        con.execute(d)
    except Exception as e:
        con.close()
        logger.error('Failed to upload to ftp: ' + str(e) + " Username: " + firstName + " URL: " + request.base_url)
    con.close()
    return redirect(url_for('cart'))


@app.route("/account/profil")
def accountProfil():
    loggedIn, firstName= getLoginDetails()
    typeData, manuData, catData = xyz()
    item_no = item_number()
    return render_template('index.html', categoryData=catData, typeData = typeData, manuData = manuData, noOfItems=item_no, loggedIn = loggedIn)


@app.route("/account/orders")
def accountOrders():
    loggedIn, firstName= getLoginDetails()
    typeData, manuData, catData = xyz()
    item_no = item_number()
    con = engine.connect()
    try:
        email = session['email']
        client = metadata.tables['client']
        select_clientId = select([client]).where(client.c.email == email)
        client_data = con.execute(select_clientId).fetchall()

        for row in client_data:
            clientId = row.clientId

        orders = metadata.tables['orders']
        delivery = metadata.tables['delivery']
        payment = metadata.tables['payment']
        join_ord = orders.join(delivery, orders.c.deliveryId == delivery.c.deliveryId)
        ord_sel = select([orders.c.deliveryId, orders.c.productName, orders.c.valueGross, orders.c.quantity, delivery.c.deliveryType]).select_from(join_ord).where(orders.c.clientId == clientId)
        productData = con.execute(ord_sel).fetchall()
    except Exception as e:
        con.close()
        logger.error('Failed to upload to ftp: ' + str(e) + " Username: " + firstName + " URL: " + request.base_url)
    con.close()
    return render_template("index.html", orders=productData, categoryData=catData, typeData = typeData, manuData = manuData, noOfItems=item_no, loggedIn = loggedIn)



@app.route("/registerForm", methods = ['GET', 'POST'])
def registerForm():
    item_no = item_number()
    con = engine.connect()
    try:
        product = metadata.tables['product']
        meta = select([product])
        products = con.execute(meta)
    except Exception as e:
        con.close()
        logger.error('Failed to upload to ftp: ' + str(e) + " Username: " + "TEST" + " URL: " + request.base_url)
    con.close()
    typeData, manuData, catData = xyz()
    return render_template('register.html', categoryData=catData, typeData = typeData, manuData = manuData, noOfItems=item_no, productData=products)


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
                try:
                    client = metadata.tables['client']
                    client_insert = client.insert().values(
                        firstName=firstName,
                        lastName=lastName,
                        clientAddress=address,
                        email=email,
                        phone=tel,
                        deliveryId = 1,
                        paymentId = 1,
                        password = hashlib.md5(password.encode()).hexdigest())
                    save = con.execute(client_insert)
                except Exception as e:
                    con.close()
                    logger.error('Failed to upload to ftp: ' + str(e) + " Username: " + firstName + " URL: " + request.base_url)
                con.close()
            return redirect(url_for('root'))

@app.route("/loginForm", methods=['GET', 'POST'])
def loginForm():
    item_no = item_number()
    con = engine.connect()
    try:
        product = metadata.tables['product']
        meta = select([product])
        products = con.execute(meta)
    except Exception as e:
        con.close()
        logger.error('Failed to upload to ftp: ' + str(e) +  " URL: " + request.base_url)
    con.close()
    typeData, manuData, catData = xyz()
    return render_template('login.html', categoryData=catData, typeData = typeData, manuData = manuData, noOfItems=item_no, productData=products)


def is_valid(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM client')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False


@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('root'))
        else:
            logger.error('Failed to upload to ftp: ' + request.base_url)


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('root'))

if __name__ == '__main__':
    app.run(debug=True, port= '8080')
    #engine.dispose()