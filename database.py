import sqlite3

# Open database
conn = sqlite3.connect('database.db')

# Create table
conn.execute('''CREATE TABLE IF NOT EXISTS client 
		(clientId INTEGER PRIMARY KEY, 
        firstName TEXT,
		lastName TEXT,
        clientAddress TEXT,
		email TEXT,
        phone TEXT,
		deliveryId INTEGER,
        paymentId INTEGER,
		FOREIGN KEY(deliveryId) REFERENCES delivery(deliveryId),
        FOREIGN KEY(paymentId) REFERENCES payment(paymentId)
		)''')

conn.execute('''CREATE TABLE IF NOT EXISTS product
		(productId INTEGER PRIMARY KEY,
		productName TEXT,
        description TEXT,
        typeId INTEGER,
        categoryId INTEGER,
        manufacturerId INTEGER,
        warrantyId,
        taxId INTEGER,
		priceNet REAL,
        priceGross REAL,
        FOREIGN KEY(typeId) REFERENCES type(typeId),
		FOREIGN KEY(categoryId) REFERENCES category(categoryId),
        FOREIGN KEY(manufacturerId) REFERENCES manufacturer(manufacturerId),
        FOREIGN KEY(warrantyId) REFERENCES warranty(warrantyId),
        FOREIGN KEY(taxId) REFERENCES taxation(taxId)
		)''')

conn.execute('''CREATE TABLE IF NOT EXISTS category
		(categoryId INTEGER PRIMARY KEY,
		name TEXT
		)''')


conn.execute('''CREATE TABLE IF NOT EXISTS type
        (typeId INTEGER PRIMARY KEY,
        name TEXT
        )''')

conn.execute('''CREATE TABLE IF NOT EXISTS manufacturer
        (manufacturerId INTEGER PRIMARY KEY,
        name TEXT
        )''')

conn.execute('''CREATE TABLE IF NOT EXISTS warranty
        (warrantyId INTEGER PRIMARY KEY,
        warranty TEXT,
        duration INTEGER,
        resignationTime INTEGER
        )''')

conn.execute('''CREATE TABLE IF NOT EXISTS taxation
        (taxId INTEGER PRIMARY KEY,
        taxPercentage REAL,
        taxBase INTEGER,
        discountPercentage REAL,
        discountBase
        )''')

conn.execute('''CREATE TABLE IF NOT EXISTS errorLog
        (errorId INTEGER PRIMARY KEY,
        date TEXT,
        description TEXT,
        IP TEXT,
        URL TEXT,
        session TEXT
        )''')

conn.execute('''CREATE TABLE IF NOT EXISTS payment
		(paymentId INTEGER PRIMARY KEY,
		paymentType TEXT
		)''')

conn.execute('''CREATE TABLE IF NOT EXISTS delivery
		(deliveryId INTEGER PRIMARY KEY,
		deliveryType TEXT,
        duration TEXT
		)''')

conn.execute('''CREATE TABLE IF NOT EXISTS warehouse
		(warehouseId INTEGER PRIMARY KEY,
		name TEXT,
        address TEXT,
        idNip INTEGER,
        FOREIGN KEY(idNip) REFERENCES company(idNip)
		)''')

conn.execute('''CREATE TABLE IF NOT EXISTS company
		(idNip INTEGER PRIMARY KEY,
        regon INTEGER,
        krs INTEGER,
		name TEXT,
        address TEXT,
        phone TEXT,
        email TEXT
		)''')

conn.execute('''CREATE TABLE IF NOT EXISTS availability
		(warehouseId INTEGER,
        productId INTEGER,
		state INTEGER,
        FOREIGN KEY(warehouseId) REFERENCES warehouse(warehouseId),
        FOREIGN KEY(productId) REFERENCES product(productId)
		)''')

conn.execute('''CREATE TABLE IF NOT EXISTS orders
		(orderID INTEGER PRIMARY KEY,
		productId INTEGER,
        productName TEXT,
        categoryId INTEGER,
        clientId INTEGER,
        clientAddress TEXT,
        idNip INTEGER,
        deliveryId INTEGER,
        paymentId INTEGER,
        date TEXT,
        quantity INTEGER,
        valueNet REAL,
        valueGross REAL,
        FOREIGN KEY(productId) REFERENCES product(productId),
        FOREIGN KEY(productName) REFERENCES product(productName),
        FOREIGN KEY(categoryId) REFERENCES product(categoryId),
        FOREIGN KEY(clientId) REFERENCES client(clientId),
        FOREIGN KEY(clientAddress) REFERENCES client(clientAddress)
        FOREIGN KEY(idNip) REFERENCES company(idNip),
        FOREIGN KEY(deliveryId) REFERENCES client(deliveryId),
        FOREIGN KEY(paymentId) REFERENCES client(paymentId)
		)''')

conn.execute('''CREATE TABLE IF NOT EXISTS cart
		(clientId INTEGER,
		productId INTEGER,
		quantity INTEGER,
		FOREIGN KEY(clientId) REFERENCES client(clientId),
		FOREIGN KEY(productId) REFERENCES product(productId)
		)''')

conn.close()

def add():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    type = [(20, 'Silniki'),
            (21, 'Świece'),
            (23, 'Filtry powietrza'),
            (24, 'Oleje'),
            (25, 'Klocki hamulcowe')
            ]
    category =   [(21, 'Orginalne'),
                (22, 'Zamienniki'),
                 ]
    manufacturer = [(21, 'Bosch'),
                    (22, 'Castrol'),
                    (23, 'Motul'),
                    (24, 'Sachs'),
                    (25, 'Volkswagen'),
                    ]
    #ID, Nazwa produktu, Opis, Typ, Kategoria, Producent, ?, ?, Cena netto, Cena brutto
    product = [(3, "Silnik 1.9 TDI", "Silnik do Audi A4/A6 B5", 20, 22, 25, 3, 3, 1000, 1230),
               (4, "Olej syntetyczny Castrol EDGE", "Olej do samochodów osobowych", 24, 21, 22, 4, 4, 20, 24.6),
               (5, "Silnik 1.8 ADR", "Silnik do Audi A4 B5", 20, 22, 25, 3, 3, 2000, 2460),
               (6, "Silnik 1.8 AGN", "Silnik do Audi A3 8L", 20, 22, 25, 3, 3, 1000, 1230),
               (7, "Klocki hamulcowe BOSCH ", "Klocki hamulcowe uniwersalne do różnych typów samochodów", 25, 21, 21, 3, 3, 10, 12.3),
               (8, "Świece BOSCH PLATINUM IRIDIUM FR7KI332S ", "Świece zapłonowe uniwersalne", 21, 21, 21, 3, 3, 20, 24.6),
               (9, "Świece BOSCH FR6KI332S", "Świece zapłonowe uniwersalne", 21, 21, 21, 3, 3, 30, 36.9),
               (10, "Motul Air Filter MHX77D", "Filtr powietrza do sam. osobowych", 23, 21, 23, 3, 3, 30, 36.9),
               (11, "MOTUL 5100 MA2 4T 10W40", "Olej syntetyczny, obj. 4L", 24, 21, 23, 3, 3, 100, 123),
               (12, "MOTUL 51012 MA2 4T 10W50", "Olej syntetyczny, obj. 5L", 24, 21, 23, 3, 3, 100, 123),
               (13, "Olej syntetyczny Castrol 18B20", "Olej do półsyn. do sam. osobowych", 24, 21, 22, 4, 4, 30, 36.9),
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
    conn.close()

add()