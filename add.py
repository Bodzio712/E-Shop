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
    category =   [(21, 'Orginalne'),
                (22, 'Zamienniki'),
                 ]
    manufacturer = [(21, 'Bosch'),
                    (22, 'Castrol'),
                    (23, 'Motul'),
                    (24, 'Sachs'),
                    ]
    product = [(3, "produkt3", "Opis3", 20, 21, 21, 3, 3, 100, 150),
               (4, "produkt4", "Opis4", 21, 22, 22, 4, 4, 300, 220),

            ]
#c.executemany('INSERT INTO type VALUES (?,?)', type)
 #   c.executemany('INSERT INTO category VALUES (?,?)', category)
 #   c.executemany('INSERT INTO manufacturer VALUES (?,?)', manufacturer)
    c.executemany('INSERT INTO product VALUES (?,?,?,?,?,?,?,?,?,?)', product)
    conn.commit()

add()