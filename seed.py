import csv
import os
from app import app, db
from products.models import Product
import sqlite3


def db_execute(query):
    with app.app_context():
        db.session.execute(query)


def db_query(query):
    with app.app_context():
        return db.session.execute(query).all()


def create_product(row):
    """
    create a product. maps field names from the sample csv to the column names
    """
    product = Product(
        name=row["product_name"],
        retail_price=row["retail_price"],
        discounted_price=row["discounted_price"],
        flipkart_advantage=row["is_FK_Advantage_product"],
        rating=row["product_rating"],
        overall_rating=row["overall_rating"],
        product_specifications=row["product_specifications"],
    )
    db.session.add(product)
    return product


def create_categories(row, product):
    categories = row["product_category_tree"]
    categories = categories.replace('["', "").replace('"]', "")
    for category in categories.split(">>"):
        name = category.strip()
        existing = db_query("SELECT * FROM categories WHERE name = ?", (name,))
        if not existing:
            existing = db_execute(
                "INSERT INTO categories (name) VALUES (?) RETURNING *", (category,)
            )[0]
        # create product category
        db_execute(
            "INSERT INTO product_categories (product_id, category_id) VALUES (:product_id, :category_id)",
            {
                "product_id": product["id"],
                "category_id": existing["id"],
            },
        )


def create_images(row, product):
    images = row["image"]
    images = images.replace('["', "").replace('"]', "")
    for url in images.split('", "'):
        db_execute(
            "INSERT INTO images (url, product_id) VALUES (:url, :product_id)",
            {"url": url, "product_id": product["id"]},
        )


def create_brand(row, product):
    brand = row["brand"]
    existing = db_query("SELECT * FROM brands WHERE name = ?", (brand,))
    if not existing:
        existing = db_execute(
            "INSERT INTO brands (name) VALUES (?) RETURNING *", (brand,)
        )[0]
    # create product brand
    db_execute(
        "INSERT INTO product_brands (product_id, brand_id) VALUES (:product_id, :brand_id)",
        {
            "product_id": product["id"],
            "brand_id": existing["id"],
        },
    )


import pprint

pp = pprint.PrettyPrinter(indent=4)


def seed():
    count = 0
    with open("flipkart_com-ecommerce_sample.csv") as fk_csv:
        products_csv = csv.DictReader(fk_csv)
        for row in products_csv:
            if count % 1000 == 0:
                # we know the sample has 20k rows, https://www.kaggle.com/datasets/PromptCloudHQ/flipkart-products
                print(f"handling row {count} of 20000")
            count += 1
            try:
                product = create_product(row)
                create_categories(row, product)
                create_images(row, product)
                create_brand(row, product)
            except sqlite3.IntegrityError:
                print("Could not insert row (Integrity Error)", row)


if __name__ == "__main__":
    input("drop database? (enter to continue, cmd+c to exit)")
    os.remove("./products.db")
    import initdb

    input("create data from sample csv (enter to continue, cmd+c to exit)")
    print("creating data. may take a few minutes...")
    seed()
