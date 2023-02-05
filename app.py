from flask import Flask, render_template, request, redirect, abort
from products.db import search_products, select_product_by_id_with_details

app = Flask(__name__)

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
    products = search_products()
    return render_template('search.html', products=products)

@app.get('/products/<product_id>')
def show_product(product_id):
    product = select_product_by_id_with_details(product_id)
    if not product:
        abort(404, "No product with that id")
    return render_template("product.html", product=product)
