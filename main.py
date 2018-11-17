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
from models.models import *

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



@app.route("/", methods=['POST', 'GET'])
def root():
    return render_template('index.html')


@app.route("/load_products", methods=['POST', 'GET'])
def load_products():
    if request.method == 'GET':
        model = ProductModel()
        products = (model.get_product())
        xa = json.dumps([dict(r) for r in products])
        return jsonify(xa)
    return redirect(url_for('root'))

@app.route("/load_types", methods=['POST', 'GET'])
def load_types():
    model = TypeModel()
    types = (model.get_product())
    xa = json.dumps([dict(r) for r in types])
    return jsonify(xa)

@app.route("/load_manufacturers", methods=['POST', 'GET'])
def load_manufacturers():
    model = ManufacturerModel()
    manufacturers = (model.get_product())
    xa = json.dumps([dict(r) for r in manufacturers])
    return jsonify(xa)

@app.route("/load_categories", methods=['POST', 'GET'])
def load_categories():
    model = CategoryModel()
    categories = (model.get_product())
    xa = json.dumps([dict(r) for r in categories])
    return jsonify(xa)

#######--------Cart functions
        # @app.route("/add_to_cart/<id>", methods=['POST', 'GET', 'PUT'])
        # def add_to_cart():
        #     clientId = str(id)
        #     #productId, quantity tak samo!!!
        #     model = CartModel()
        #     add = (model.add_cart(clientId, productId, quantity))
        #     return add
        #
        # @app.route("/remove_from_cart/<id>", methods=['POST', 'GET'])
        # def remove_from_cart():
        #     cartId = str(id)
        #     model = CartModel()
        #     remove = (model.remove_from_cart(cartId))
        #     xa = json.dumps(remove)
        #     return jsonify(xa)

@app.route("/display_cart", methods=['POST', 'GET'])
def get_cart_details():
    model = CartModel()
    details = (model.get_cart_details())
    xa = json.dumps([dict(r) for r in details])
    return jsonify(xa)

@app.route("/delete_cart", methods=['POST', 'GET', 'DELETE'])
def delete_cart():
    model = CartModel()
    delete = (model.delete_cart())
    return delete

@app.route("/item_number", methods=['POST', 'GET'])
def item_number():
    model = CartModel()
    item_number = (model.item_number())
    xa = json.dumps(item_number)
    return jsonify(xa)




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
    app.run(debug=True, port='8080')
    #engine.dispose()