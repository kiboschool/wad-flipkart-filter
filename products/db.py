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
def db_query(query, args=(), one=False):
    conn = get_connection()
    cur = conn.execute(query, args)
    results = cur.fetchall()
    cur.close()
    conn.close()
    if one:
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

PER_PAGE = 40
def search_products(params):
    filter = " WHERE 1 = 1 "
    if params['brands']:
        # filter to only the products from those brands
        brand_results = db_query("SELECT product_brands.product_id FROM brands JOIN product_brands ON product_brands.brand_id = brands.id WHERE brands.name LIKE ?", params['brands'])
        for (i, val) in enumerate(brand_results, start=0):
            params["brand_id_"+str(i)] = val['product_id']
        filter = " WHERE id IN (" + ','.join([":brand_id_"+str(i) for i in range(len(brand_results))]) +") "

    # if params['categories']:
        #"categories": request.values.getlist('category'),

    sort_to_order = {
        "price-low": "discounted_price ASC",
        "price-high": "discounted_price DESC",
        "rating": "rating DESC",
        "relevance": "id ASC",
        "discount": "CEIL(retail_price / discounted_price) DESC"
    }
    if params["q"]:
        filter += " AND name LIKE :query "
        params["query"] = f"%{params['q']}%"
    if params["price_min"]:
        filter += " AND discounted_price > :price_min "
    if params["price_max"] and params["price_max"].isnumeric():
        filter += " AND discounted_price < :price_max "
    if params["fk_advantage"]:
        filter += " AND flipkart_advantage = 'true'"
    if params["ratings"]:
        if '2' in params['ratings']:
            filter += " AND rating > 2"
        elif '3' in params['ratings']:
            filter += " AND rating > 3"
        elif '4' in params['ratings']:
            filter += " AND rating > 4"

    order = " ORDER BY " + sort_to_order.get(params['sort'], "id ASC ")
    products_query = "SELECT * FROM products "
    # pagination is hard without https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/pagination/
    params["offset"] = params['page'] * PER_PAGE
    params["limit"] = PER_PAGE

    results = db_query(products_query + filter + order + " LIMIT :limit OFFSET :offset;", params)
    select_images(results)
    count_query = "SELECT COUNT(*) FROM products "
    count = db_query(count_query + filter, params, one=True)['COUNT(*)']
    return results, count

# supplements the product search results with the associated images
def select_images(products):
    images_query = "SELECT * FROM images WHERE images.product_id IN (" + \
        ("?,"*len(products))[:-1] + ") GROUP BY images.product_id"
    image_results = db_query(images_query, [r['id'] for r in products])
    products_by_id = { product['id'] : product for product in products}
    for image in image_results:
        products_by_id[image['product_id']]['image'] = image

def select_product_by_id_with_details(_id):
    product = db_query("SELECT * FROM products WHERE products.id = ? LIMIT 1;", (_id,), one=True)
    if not product:
        return None
    product['images'] = db_query("SELECT * FROM images WHERE images.product_id = ?;", (_id,))
    product['brand'] = db_query("SELECT brands.name FROM product_brands JOIN brands ON product_brands.brand_id = brands.id WHERE product_brands.product_id = ?;", (_id,), one=True)
    product['categories'] = db_query("SELECT categories.name FROM product_categories JOIN categories ON product_categories.category_id = categories.id WHERE product_categories.product_id = ?;", (_id,))
    return product
