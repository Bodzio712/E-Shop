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
    return (loggedIn, firstName, userId)



@app.route("/", methods=['POST', 'GET'])
def root():
    return render_template('index.html')


@app.route("/is_logged", methods=['POST', 'GET'])
def is_logged():
    data = {}
    if 'email' not in session:
        data['isLogged'] = 'false'
    else:
        data['isLogged'] = 'true'
    json_data = json.dumps(data)
    return jsonify(json_data)


@app.route("/load_products", methods=['POST', 'GET'])
def load_products():
    if request.method == 'GET':
        model = ProductModel()
        products = (model.get_product())
        xa = json.dumps([dict(r) for r in products])
        #print(xa)
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

#####################Cart functions#####################
@app.route("/cart")
def cart():
    loggedIn, firstName, userId = getLoginDetails()
    if loggedIn == True:
        return render_template("cart.html")
    else:
        return redirect(url_for('root'))

@app.route("/addToCart", methods=['POST', 'GET', 'PUT'])
def add_to_cart():
    productId = int(request.args.get('productId'))
    loggedIn, firstName, userId = getLoginDetails()
    quantity = request.form['liczba']
    print(productId, userId, quantity)
    model = CartModel()
    add = (model.add_cart(userId, productId, quantity))
    print(add)
    if add == True:
        return redirect(url_for('cart'))
    else:
        return redirect(url_for('root')) #zmienic na jakies 404

@app.route("/removeCart", methods=['POST', 'GET'])
def remove_from_cart():
    cartId = int(request.args.get('cartId'))
    model = CartModel()
    remove = (model.remove_from_cart(cartId))
    print(remove)
    dele = json.dumps(remove)
    print(dele)
    return redirect(url_for('cart'))


@app.route("/display_cart", methods=['POST', 'GET'])
def get_cart_details():
    model = CartModel()
    details = (model.get_cart_details())
    xa = json.dumps([dict(r) for r in details])
    print(xa)
    return jsonify(xa)

@app.route("/display_cart_items", methods=['POST', 'GET'])
def get_cart():
    model = CartModel()
    details = (model.get_cart())
    xa = json.dumps([dict(r) for r in details])
    return jsonify(xa)

@app.route("/display_orders", methods=['POST', 'GET'])
def get_orders():
    model = OrdersModel()
    details = (model.get_orders())
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

@app.route("/delivery_details", methods=['POST', 'GET'])
def delivery_detalis():
    model = CartModel()
    delivery_data = (model.get_delivery_info())
    xa = json.dumps([dict(r) for r in delivery_data])
    return jsonify(xa)

@app.route("/payment_details", methods=['POST', 'GET'])
def payment_detalis():
    model = CartModel()
    payment_data = (model.get_payment_info())
    xa = json.dumps([dict(r) for r in payment_data])
    return jsonify(xa)


@app.route("/placeOrder", methods=["POST"])
def placeOrder():
    loggedIn, firstName, userId = getLoginDetails()
    print("jestem w place order")
    try:
        deliveryId = request.form['delivery-collection'],
        paymentId = request.form['payment-collection'],
        email = session['email']
        model = placeOrder()
        print("jestem w modelu")
        status = (model.placeorder(deliveryId, paymentId, email))
        print("Stats")
        print(status)
        if status == True:
            delete_cart()
            return redirect(url_for('root'))
    except Exception as e:
        logger.error('Failed to upload to ftp: ' + str(e) + " Username: " + firstName + " URL: " + request.base_url)
        return redirect(url_for('cart'))

############# Logowanie#################
@app.route("/account/orders")
def accountOrders():
    return render_template("orders.html")

@app.route("/registerForm", methods = ['GET', 'POST'])
def registerForm():
    return render_template('register.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
            if request.method == 'POST':
                # Parse form data
                password = request.form['password']
                cpassword = request.form['cpassword']
                email = request.form['email']
                firstName = request.form['firstName']
                lastName = request.form['lastName']
                address = request.form['address']
                tel = request.form['phone']

                if password == cpassword:
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
                    return redirect(url_for('loginForm'))
                return redirect(url_for('registerForm'))

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
    return render_template('login.html')


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
    app.run(debug=True, port='8888')
    #engine.dispose()