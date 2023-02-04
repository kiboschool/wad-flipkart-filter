from flask import Flask, render_template, request, g, redirect, abort
from products.db import get_paged_products, select_product_by_id_with_details

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
    return render_template('index.html')

@app.get('/search')
def search():
    # page = ?
    # brand = ?
    # categories = ?
    # search = ?
    # price_min = ?
    # price_max = ?
    # sort = ?
    products = get_paged_products()
    return render_template('search.html', products=products)

@app.get('/products/<product_id>')
def show_product(product_id):
    product = select_product_by_id_with_details(product_id)
    if not product:
        abort(404, "No product with that id")
    return render_template("product.html", product=product)
