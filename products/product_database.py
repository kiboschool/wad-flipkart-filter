from sqlalchemy import select
from sqlalchemy.orm import selectinload
from products.models import Product


class ProductDatabase:
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
        if params["q"]:
            q = q.filter(Product.name.like(f"%{params['q']}%"))
        if params["price_min"]:
            q = q.filter(Product.discounted_price > params["price_min"])
        if params["price_max"]:
            q = q.filter(Product.discounted_price < params["price_max"])
        if params["fk_advantage"]:
            q = q.filter(Product.flipkart_advantage == True)
        if params["ratings"]:
            q = q.filter(Product.rating > params["ratings"])

        sort_to_order = {
            "price-low": Product.discounted_price.asc(),
            "price-high": Product.discounted_price.desc(),
            "rating": Product.rating.desc(),
            "relevance": Product.id.asc(),
            "discount": Product.discount.desc(),
        }
        if params["sort"] and params["sort"] in sort_to_order:
            q = q.order_by(sort_to_order[params["sort"]])

        # always include images, categories, brands
        q = (
            q.options(selectinload(Product.categories))
            .options(selectinload(Product.brands))
            .options(selectinload(Product.images))
        )
        # paginate the results
        return self.db.paginate(q, per_page=ProductDatabase.PER_PAGE)
