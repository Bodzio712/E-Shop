import sqlite3

# Open database
conn = sqlite3.connect('database.db')

# Create table
conn.execute('''CREATE TABLE client 
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

conn.execute('''CREATE TABLE product
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

conn.execute('''CREATE TABLE category
		(categoryId INTEGER PRIMARY KEY,
		name TEXT
		)''')


conn.execute('''CREATE TABLE type
        (typeId INTEGER PRIMARY KEY,
        name TEXT
        )''')

conn.execute('''CREATE TABLE manufacturer
        (manufacturerId INTEGER PRIMARY KEY,
        name TEXT
        )''')

conn.execute('''CREATE TABLE warranty
        (warrantyId INTEGER PRIMARY KEY,
        warranty TEXT,
        duration INTEGER,
        resignationTime INTEGER
        )''')

conn.execute('''CREATE TABLE taxation
        (taxId INTEGER PRIMARY KEY,
        taxPercentage REAL,
        taxBase INTEGER,
        discountPercentage REAL,
        discountBase
        )''')

conn.execute('''CREATE TABLE errorLog
        (errorId INTEGER PRIMARY KEY,
        date TEXT,
        description TEXT,
        IP TEXT,
        URL TEXT,
        session TEXT
        )''')

conn.execute('''CREATE TABLE payment
		(paymentId INTEGER PRIMARY KEY,
		paymentType TEXT
		)''')

conn.execute('''CREATE TABLE delivery
		(deliveryId INTEGER PRIMARY KEY,
		deliveryType TEXT,
        duration TEXT
		)''')

conn.execute('''CREATE TABLE warehouse
		(warehouseId INTEGER PRIMARY KEY,
		name TEXT,
        address TEXT,
        idNip INTEGER,
        FOREIGN KEY(idNip) REFERENCES company(idNip)
		)''')

conn.execute('''CREATE TABLE company
		(idNip INTEGER PRIMARY KEY,
        regon INTEGER,
        krs INTEGER,
		name TEXT,
        address TEXT,
        phone TEXT,
        email TEXT
		)''')

conn.execute('''CREATE TABLE availability
		(warehouseId INTEGER,
        productId INTEGER,
		state TEXT,
        FOREIGN KEY(warehouseId) REFERENCES warehouse(warehouseId),
        FOREIGN KEY(productId) REFERENCES product(productId)
		)''')

conn.execute('''CREATE TABLE orders
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

conn.execute('''CREATE TABLE cart
		(clientId INTEGER,
		productId INTEGER,
		FOREIGN KEY(clientId) REFERENCES client(clientId),
		FOREIGN KEY(productId) REFERENCES product(productId)
		)''')

conn.close()
