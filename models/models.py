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

except Exception as e:
    con.close()
    #logger.error('Zaladowanie tabeli się nie powiodło:  ' + str(e) )
con.close()


class ProductModel():

    def get_product(self):
        con = engine.connect()
        product_all = con.execute(select([product])).fetchall()
        con.close()
        return product_all

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

    def get_product(self):
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


