import csv
from db import db_query, db_execute
import sqlite3

def create_product(row):
    """
    create a product. maps field names from the sample csv to the column names
    """
    try:
        return db_execute("""
        INSERT INTO products ( pid, name, retail_price, discounted_price, flipkart_advantage, rating, overall_rating, product_specifications
        ) VALUES (
            :pid, :name, :retail_price, :discounted_price, :flipkart_advantage, :rating, :overall_rating, :product_specifications
        ) RETURNING *
    """, {
        "pid": row['pid'],
        "name": row['product_name'],
        "retail_price":row['retail_price'] , 
        "discounted_price": row['discounted_price'],
        "flipkart_advantage": row['is_FK_Advantage_product'],
        "rating": row['product_rating'],
        "overall_rating": row['overall_rating'],
        "product_specifications":  row['product_specifications'],
        })

    except sqlite3.IntegrityError:
        print("Could not insert row (Integrity Error)", row)

def create_categories(row, product):
    categories = row['product_category_tree']
    categories = categories.replace('["', '').replace('"]', '')
    for category in categories.split(">>"):
        category = category.strip()
        existing = db_query("SELECT * FROM categories WHERE name = ?", (category,))
        if not existing:
            existing = db_execute("INSERT INTO categories (name) VALUES (?) RETURNING *", (category,))[0]
        # create product category
        db_execute("INSERT INTO product_categories (product_id, category_id) VALUES (:product_id, :category_id)", {
            "product_id": product['id'],
            "category_id": existing['id'],
            })

def create_images(row, product):
    images = row['image']
    images = images.replace('["', '').replace('"]', '')
    for url in images.split("\", \""):
        db_execute("INSERT INTO images (url, product_id) VALUES (:url, :product_id)", 
                   { "url": url, "product_id": product['id'] })
     
def create_brand(row, product):
    brand = row['brand']
    existing = db_query("SELECT * FROM brands WHERE name = ?", (brand,))
    if not existing:
        existing = db_execute("INSERT INTO brands (name) VALUES (?) RETURNING *", (brand,))[0]
    # create product brand
    db_execute("INSERT INTO product_brands (product_id, brand_id) VALUES (:product_id, :brand_id)", {
        "product_id": product['id'],
        "brand_id": existing['id'],
        })


import pprint
pp = pprint.PrettyPrinter(indent=4)

def seed():
    with open('flipkart_com-ecommerce_sample.csv') as fk_csv:
        products_csv = csv.DictReader(fk_csv)
        for row in products_csv:
            product = create_product(row)
            product = product[0]
            create_categories(row, product)
            create_images(row, product)
            create_brand(row, product)

def clean():
    db_execute("DELETE FROM products;", ())
    db_execute("DELETE FROM categories;", ())
    db_execute("DELETE FROM images;", ())
    db_execute("DELETE FROM brands;", ())
    db_execute("DELETE FROM product_categories;", ())
    db_execute("DELETE FROM product_brands;", ())

if __name__ == "__main__":
    clean()
    seed()
