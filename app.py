from flask import Flask, render_template, request, redirect, abort
from products.db import search_products, select_product_by_id_with_details, PER_PAGE

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/search')
def search():
    params = {
        "q": request.values.get('q'),
        "page": int(request.values.get('page', 0)),
        "brands": request.values.getlist('brand'),
        "categories": request.values.getlist('category'),
        "fk_advantage": request.values.get("fk-advantage"),
        "ratings": request.values.getlist('ratings'),
        "price_min": request.values.get('min-price'),
        "price_max": request.values.get('max-price'),
        "sort": request.values.get('sort')
    }
    products, count = search_products(params)
    return render_template('search.html', products=products, params=params, count=count, page_size=PER_PAGE)

@app.get('/products/<product_id>')
def show_product(product_id):
    product = select_product_by_id_with_details(product_id)
    if not product:
        abort(404, "No product with that id")
    return render_template("product.html", product=product)
