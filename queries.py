from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models import Product, Brand, Category


class Queries:
    PER_PAGE = 40

    def __init__(self, db):
        self.db = db

    def select_product_with_details(self, id):
        q = (
            select(Product)
            .filter(Product.id == id)
            .options(selectinload(Product.categories))
            .options(selectinload(Product.brands))
            .options(selectinload(Product.images))
        )
        return self.db.session.scalars(q).first()

    def search_products(self, params):
        q = select(Product)

        # apply filters to the base query
        # only for the search params that are present
        if params["q"]:
            q = q.filter(Product.name.like(f"%{params['q']}%"))

        if params["price_min"]:
            q = q.filter(Product.discounted_price > params["price_min"])

        if params["price_max"]:
            q = q.filter(Product.discounted_price < params["price_max"])

        if params["ratings"]:
            for rating in params["ratings"]:
                q = q.filter(Product.rating > rating)

        if params["fk_advantage"] in ["on", "true", "checked"]:
            q = q.filter(Product.flipkart_advantage == "true")

        if params["categories"]:
            # join to categories table
            q = q.join(Product.categories)
            for category in params["categories"]:
                # filter where category param is LIKE the category name
                q = q.filter(Category.name.like(f"%{category}%"))

        if params["brands"]:
            q = q.join(Product.brands)
            for brand in params["brands"]:
                q = q.filter(Brand.name.like(f"%{brand}%"))

        # order the results
        if params["sort"]:
            q = self._order_results(q, params["sort"])

        # eager load images, categories, and brands
        # See https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html#select-in-loading
        q = (
            q.options(selectinload(Product.categories))
            .options(selectinload(Product.brands))
            .options(selectinload(Product.images))
        )

        # paginate the results
        # limit of 40 items PER_PAGE
        # uses flask-sqlalchemy's built-in pagination
        # See https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/pagination/
        return self.db.paginate(q, per_page=Queries.PER_PAGE)

    def _order_results(self, q, sort_method):
        if sort_method == "relevance":
            return q.order_by(Product.id.asc())
        elif sort_method == "rating":
            return q.order_by(Product.rating.desc())
        elif sort_method == "discount":
            return q.order_by(Product.discount.desc())
        elif sort_method == "price-low":
            return q.order_by(Product.discounted_price.asc())
        elif sort_method == "price-high":
            return q.order_by(Product.discounted_price.desc())
