from flask import Flask, render_template, request, abort
from queries import Queries
from models import db

app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../products.db"

# enable logging SQL queries
# app.config["SQLALCHEMY_ECHO"] = True

# initialize the app with the extension
db.init_app(app)
queries = Queries(db)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/products/<product_id>")
def show_product(product_id):
    product = queries.select_product_with_details(product_id)
    if not product:
        abort(404, "No product with that id")
    return render_template("product.html", product=product)


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
    products = queries.search_products(params)
    return render_template("search.html", products=products, params=params)
