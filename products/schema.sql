CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pid TEXT UNIQUE,
  name TEXT,
  retail_price INTEGER,
  discounted_price INTEGER,
  flipkart_advantage BOOLEAN,
  rating INTEGER,
  overall_rating INTEGER,
  product_specifications TEXT
);

CREATE TABLE categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE product_categories (
  product_id INTEGER NOT NULL REFERENCES products(id),
  category_id INTEGER NOT NULL REFERENCES categories(id)
);

CREATE TABLE images (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id INTEGER NOT NULL,
  url TEXT NOT NULL
);

CREATE TABLE brands (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE product_brands (
  product_id INTEGER NOT NULL REFERENCES products(id),
  brand_id INTEGER NOT NULL REFERENCES brands(id)
);
