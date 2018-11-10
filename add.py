# -*- coding: utf-8 -*-
from flask import *
from peewee import *
import sqlite3
import os
import werkzeug
from sqlalchemy import *

def add():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    type = [(20, 'Silniki'),
            (21, 'Świece'),
            (23, 'Lusterka')
             ]
    cat =   [(21, 'Orginalne'),
            (22, 'Zamienniki'),
             ]
    manu = [(21, 'Bosch'),
            (22, 'Castrol'),
            (23, 'Motul'),
            (24, 'Sachs'),
             ]
    c.executemany('INSERT INTO type VALUES (?,?)', type)
    c.executemany('INSERT INTO category VALUES (?,?)', cat)
    c.executemany('INSERT INTO manufacturer VALUES (?,?)', manu)
    conn.commit()

add()