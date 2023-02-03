# Product Interface
import sqlite3

DATABASE_FILE = 'products.db'

def get_connection():
    connection = sqlite3.connect('products.db')
    connection.row_factory = sqlite3.Row
    return connection

# return the results from a database query
def db_query(query, args=()):
    conn = get_connection()
    cur = conn.execute(query, args)
    results = cur.fetchall()
    cur.close()
    conn.close()
    if len(results) == 1:
        return results[0]
    else:
        return results

# execute a database query
def db_execute(script, args):
    conn = get_connection()
    res = conn.execute(script, args).fetchall()
    conn.commit()
    conn.close()
    return res

def select_all_products():
    cursor = connection.execute("SELECT * FROM products;")
    return cursor.fetchall()

def select_product_by_id(_id):
    cursor = connection.execute("SELECT * FROM products WHERE id = ?;", [_id])
    return cursor.fetchone()

def products_cheaper_than(min_price):
    cursor = connection.execute("SELECT * FROM products WHERE price < ?;", [min_price])
    return cursor.fetchall()

def get_last_product():
    cursor = connection.execute("SELECT * FROM products ORDER BY id DESC LIMIT 1;")
    return cursor.fetchone()

def add_product(name, price, quantity):
    connection.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?);", [name, price, quantity])
    connection.commit()
    last_product = get_last_product()
    return last_product

def product_details(product):
    return f"{product['name']}: ${product['price']}. {product['quantity']} left in stock"

def product_overview(product):
    return f"{product['id']}    {product['name']}"
