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
engine = create_engine("sqlite:///database.db",
                            connect_args={'check_same_thread':False},
                            poolclass=StaticPool)
metadata = MetaData(engine, reflect=True)

con = engine.connect()
try:
    type = metadata.tables['type']
    manu = metadata.tables['manufacturer']
    cat = metadata.tables['category']
    product = metadata.tables['product']
    cart = metadata.tables['cart']
    delivery = metadata.tables['delivery']
    payment = metadata.tables['payment']
    order = metadata.tables['orders']
    client = metadata.tables['client']

except Exception as e:
    con.close()
    #logger.error('Zaladowanie tabeli się nie powiodło:  ' + str(e) )
con.close()


class OrdersModel():

    def get_orders(self):
        con = engine.connect()
        join_obj = order.join(delivery, order.c.deliveryId == delivery.c.deliveryId)
        join_sel = select([order.c.orderID, order.c.valueGross, order.c.quantity, order.c.productName, order.c.date, delivery.c.deliveryType, order.c.deliveryId]).select_from(join_obj)  # select statement
        order_all = con.execute(join_sel).fetchall()
        con.close()
        return order_all


class ProductModel():

    def get_product(self):
        con = engine.connect()

        join_obj = product.join(manu, product.c.manufacturerId == manu.c.manufacturerId)
        join_sel = select([product.c.productId, product.c.productName, product.c.description, product.c.categoryId, product.c.manufacturerId, product.c.typeId, product.c.priceNet, product.c.priceGross, manu.c.name]).select_from(join_obj)  # select statement
        details = con.execute(join_sel).fetchall()  # fetch data

        #product_all = con.execute(select([product])).fetchall()
        con.close()
        return details

class TypeModel():

    def get_product(self):
        con = engine.connect()
        type_all = con.execute(select([type])).fetchall()
        con.close()
        return type_all

class ManufacturerModel():

    def get_product(self):
        con = engine.connect()
        manu_all = con.execute(select([manu])).fetchall()
        con.close()
        return manu_all

class CategoryModel():

    def get_product(self):
        con = engine.connect()
        cat_all = con.execute(select([cat])).fetchall()
        con.close()
        return cat_all

class CartModel():

    def get_cart(self):
        con = engine.connect()
        product_all = con.execute(select([cart])).fetchall()
        con.close()
        return product_all

    def delete_cart(self):
        try:
            con = engine.connect()
            cart_delete = delete(cart)
            con.close()
            return True
        except Exception as e:
            con.close()

    def add_cart(self, clientId, productId, quantity):
        try:
            con = engine.connect()
            clientId, productId, quantity = clientId, productId, quantity
            insert = cart.insert().values(clientId=clientId, productId=productId, quantity=quantity)
            x = con.execute(insert)
            con.close()
            return True
        except Exception as e:
            con.close()


    def item_number(self):
        try:
            con = engine.connect()
            item_number = con.execute("SELECT count(productId) FROM cart").fetchone()[0]
            con.close()
            return item_number
        except Exception as e:
            con.close()

    def get_delivery_info(self):
        try:
            con = engine.connect()
            #Pobieranie z bazy danych o metodach dostawy
            select_delivery = select([delivery])
            delivery_data = con.execute(select_delivery).fetchall()
            return delivery_data
        except Exception as e:
            con.close()

    def get_payment_info(self):
        try:
            con = engine.connect()
            #Pobieranie z bazy danych o metodach dostawy
            select_payment = select([payment])
            payment_data = con.execute(select_payment).fetchall()
            return payment_data
        except Exception as e:
            con.close()


    def get_cart_details(self):
        try:
            con = engine.connect()
            #Pobieranie detali
            join_obj = cart.join(product, product.c.productId == cart.c.productId)
            join_sel = select(
                [product.c.productId, product.c.productName, product.c.description, product.c.manufacturerId, cart.c.cartId, cart.c.quantity,
                 product.c.priceNet, product.c.priceGross]).select_from(join_obj)  # select statement
            details = con.execute(join_sel).fetchall()  # fetch data

            # #Pobieranie z bazy danych o metodach dostawy
            # select_delivery = select([delivery])
            # delivery_data = con.execute(select_delivery).fetchall()
            #
            # #Pobieranie z bazy danych o metodach płatności
            # select_payment = select([payment])
            # payment_data = con.execute(select_payment).fetchall()
            return details#, delivery_data, payment_data
        except Exception as e:
            con.close()

    def remove_from_cart(self, cartId):
        try:
            con = engine.connect()
            removeId = cartId
            rem = delete(cart, cart.c.cartId == removeId, )
            con.execute(rem)
            return True
        except Exception as e:
            con.close()


class OrderModel():

    def placeorder(self, deliveryId, paymentId, email):
        with engine.connect() as connection:
            try:
                join_obj = product.join(cart, product.c.productId == cart.c.productId)
                join_sel = select(
                    [product.c.productId, product.c.productName, product.c.categoryId, product.c.priceGross, cart.c.quantity]).select_from(
                    join_obj)  # select statement
                prod_data = connection.execute(join_sel)  # fetch data

                select_clientId = select([client]).where(client.c.email == email)
                client_data = connection.execute(select_clientId).fetchall()

                for row in client_data:
                    clientId = row.clientId
                    clientAdress = row.clientAddress

                # stworz tabele orders i zapisz do bazy
                print (prod_data)
                for row in prod_data:
                    print(row)
                    ins = order.insert().values(
                        productId=row.productId,
                        productName=row.productName,
                        categoryId=row.categoryId,
                        clientId=clientId,
                        clientAddress=clientAdress,
                        idNip=1,
                        deliveryId=deliveryId,
                        paymentId=paymentId,
                        date=datetime.date.today(),
                        quantity=row.quantity,
                        valueNet=00,
                        valueGross=row.quantity*row.priceGross)
                    connection.execute(ins)
            except Exception as e:
                print(e)
                connection.close()
                return False
            connection.close()
            return True


