import sqlite3

def insertar_user(id, name, email):
    conn = sqlite3.connect('santiChelasdb.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (id, name, email)
    VALUES  (?, ?, ?)
    ''', (id, name, email)
    )
    conn.commit()
    conn.close()

def insertar_beer(name, price):
    conn = sqlite3.connect('santiChelasdb.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO beers (name, price)
    VALUES  (?, ?)
    ''', (name, price)
    )
    conn.commit()
    conn.close()

def insertar_buys(user_id, beer_id, units, payment_method):
    conn = sqlite3.connect('santiChelasdb.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO buys (user_id, beer_id, units, payment_method)
    VALUES  (?, ?, ?,?)
    ''', (user_id, beer_id, units, payment_method)
    )
    conn.commit()
    conn.close()

def leer_users():
    conn = sqlite3.connect("santiChelasdb.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def leer_beers():
    conn = sqlite3.connect("santiChelasdb.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM beers')
    beers = cursor.fetchall()
    conn.close()
    return beers

def leer_buys():
    conn = sqlite3.connect("santiChelasdb.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM buys')
    buys = cursor.fetchall()
    conn.close()
    return buys

print (leer_buys())