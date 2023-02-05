# Product Interface
import sqlite3

DATABASE_FILE = 'products/products.db'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_connection():
    connection = sqlite3.connect(DATABASE_FILE)
    connection.set_trace_callback(print)
    connection.row_factory = dict_factory
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

def search_products():
    return db_query("SELECT * FROM products LIMIT 10;")

def select_product_by_id_with_details(_id):
    product = db_query("SELECT * FROM products WHERE products.id = ? LIMIT 1;", (_id,))
    if not product:
        return None
    product['images'] = db_query("SELECT * FROM images WHERE images.product_id = ?;", (_id,))
    product['brand'] = db_query("SELECT brands.name FROM product_brands JOIN brands ON product_brands.brand_id = brands.id WHERE product_brands.product_id = ?;", (_id,))
    product['categories'] = db_query("SELECT categories.name FROM product_categories JOIN categories ON product_categories.category_id = categories.id WHERE product_categories.product_id = ?;", (_id,))
    return product
