from flask import Flask, render_template, request, g, redirect
from products.db import select_product_by_id

app = Flask(__name__)

# Get a useable connection to the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = get_connection()
    return db

# Close the database connection when the app shuts down
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.get('/')
def index():
    # page = ?
    # brand = ?
    # category = ?
    # search = ?
    # price_min = ?
    # price_max = ?
    # sort = ?
    products = get_paged_products(page)
    return render_template('index.html', products=products, page=page)

@app.get('/products/<id>')
def show_product(product_id):
    product = get_all_for_product(product_id)
    return render_template("product.html", product=product)
