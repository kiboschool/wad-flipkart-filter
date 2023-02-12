from flask import Flask, render_template, request, redirect, abort
from products.db import search_products, select_product_by_id_with_details, PER_PAGE
from products.product_database import ProductDatabase
from products.models import db

app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../products/products.db"
# app.config["SQLALCHEMY_RECORD_QUERIES"] = True
# initialize the app with the extension
db.init_app(app)
products_db = ProductDatabase(db)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/search")
def search():
    params = {
        "q": request.values.get("q"),
        "brands": request.values.getlist("brand"),
        "categories": request.values.getlist("category"),
        "fk_advantage": request.values.get("fk-advantage"),
        "ratings": request.values.getlist("ratings"),
        "price_min": request.values.get("min-price"),
        "price_max": request.values.get("max-price"),
        "sort": request.values.get("sort"),
    }
    products_page = products_db.search_products(params)
    return render_template("search.html", products=products_page, params=params)


@app.get("/products/<product_id>")
def show_product(product_id):
    product = products_db.select_product_with_details(product_id)
    if not product:
        abort(404, "No product with that id")
    return render_template("product.html", product=product)
