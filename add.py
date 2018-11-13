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
                    (25, 'Volkswagen')
                    ]
    product = [(3, "produkt3", "Opis3", 20, 21, 21, 3, 3, 100, 150),
               (4, "produkt4", "Opis4", 21, 22, 22, 4, 4, 300, 220),
               (5, "Silnik 1.8 ADR", "Silnik do Audi A4 B5", 20, 25, 25, 3, 3, 100, 150)
             ]
    state = [(1, "produkt1", 111),
               (2, "produkt2", 222),
               (3, "produkt3", 333),
               (4, "produkt4", 444),
               (2, "produkt1", 100),
               (3, "produkt2", 200),
               ]
    wh =      [(1, "warehouse1", "wh_addr_1", 123456),
               (2, "warehouse2", "wh_addr_2", 123456),
               (3, "warehouse3", "wh_addr_3", 1123456),
               (4, "warehouse4", "wh_addr_4", 123456),
               ]
    company = [(123456, 111111, 222222, "firma1", "adres_firma_1", "555-666-777", "email@firma.pl")]

    c.executemany('INSERT INTO type VALUES (?,?)', type)
    c.executemany('INSERT INTO category VALUES (?,?)', category)
    c.executemany('INSERT INTO manufacturer VALUES (?,?)', manufacturer)
    c.executemany('INSERT INTO product VALUES (?,?,?,?,?,?,?,?,?,?)', product)
    c.executemany('INSERT INTO availability VALUES (?,?,?)', state)
    c.executemany('INSERT INTO warehouse VALUES (?,?,?,?)', wh)
    c.executemany('INSERT INTO company VALUES (?,?,?,?,?,?,?)', company)
    conn.commit()

add()