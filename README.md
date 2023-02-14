# Product Pages

Relational databases are very common for E-commerce. In this project, you'll practice working with related data in multiple tables, adding features to a product pages website. You'll add missing filters to the search page, and create JSON API endpoints for products and search.

## Introduction: Fakekart

The application you'll be working on is _Fakekart_, a mini-version of [Flipkart](https://www.flipkart.com/).

Fakekart's features mostly do not work -- you can't log in, add items to the cart, or buy anything. But, the core online shopping experience still works: searching, filtering, and browsing items.

The data for this project is originally sourced from this [Kaggle dataset](https://www.kaggle.com/datasets/PromptCloudHQ/flipkart-products) by PromptCloud. Thanks Flipkart, Kaggle and PromptCloud!

## Domain

These are the tables in the database:

- products
- images
- categories
- brands

There are also two association tables:
- product_category
- product_brand

You can see the columns and relationships in `models.py`

## Starter Code

Fakekart uses Flask, Sqlite3, and [TailwindCSS](https://tailwindcss.com/).

- The application logic is in `app.py`
- The code for managing the database of products is in the `/products` folder.
- The templates are in `/templates`, with some shared components in `templates/shared`
- Static files like images and stylesheets are in `static`

Install the dependencies using pip:

```sh
pip install -r requirements.txt
```

Start the application in debug mode by running:

```sh
flask --debug run
```

and open [127.0.0.1:5000](http://127.0.0.1:5000) to view the application.

There are three routes that `app.py` serves:
- `'/'` is the index route, and it shows a landing page
- `'/products/<product_id>'` shows an individual product
- `'/search'` is a search results page

Click through all of the pages to see how they currently behave.

### Optional: Tailwind and NPM

This app uses [TailwindCSS](https://tailwindcss.com/) for styling.

The styles are pre-built in `static/styles.css`, so you should not need npm or to install anything to complete the project.

However, if you want to rebuild the styles, or if you want to edit the styles using tailwind, here's how to get started:

```sh
npm install # install the tailwind dependencies
npm run watch-styles # watch and rebuild the styles when files change
```

## Your Task

The flipkart clone is looking pretty good! It's got a database of products, and you can view a product or search the database. However, some of the search features don't work yet. You also want other developers to be able to access your application as an API.

### Part 1: Add missing filters

Right now, the search feature can filter by the name of the item, a min and max price, and by category.

Your task is to add the missing search filters and sorts:
- filter for items that are flipkart assured
- a filter for brands
- sorting by price, from low to high and high to low

For each of these features, the data is already being sent from the HTML form. **You do not need to edit the templates**. Here are the steps to update the search feature:

1. In `app.py`, add the data to the `params` that are being passed into the search helper.
2. In the `search_products` method of the Queries class in `queries.py`, add the logic to use the new filter.
  - check if the param is present
  - if the param is present, adjust it using the param to get the results you want

### Part 2: Product API

You heard that if you turn your application into an API, then it's a platform, and you can make more money.

Add API routes for showing a product and searching for a product.

- `/api/products/<product_id>` should return a JSON representation of the product
- `/api/search` should return a JSON list of search results. It should accept the same parameters as the regular `/search` route.

Both methods should use the same query as their corresponding methods, they should just return JSON results instead of showing the HTML page. You can copy and paste the `show_product` and `search` functions, and then change them to return a JSON response instead of rendering a template.

The `Product` model in `models.py` has a `.to_dict()` method that you can use to render the product in both API routes.

## Testing

Run the automated tests to check that your API routes and updated search parameters work correctly. The automated tests only look at the API routes (not the ones that render HTML).

