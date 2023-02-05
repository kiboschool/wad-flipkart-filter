# Product Pages

Relational databases are very common for E-commerce. In this project, you'll practice working with related data in multiple tables, adding features to a product pages website.

## Introduction: Fakekart

The application you'll be working on is _Fakekart_, a mini-version of [Flipkart](https://www.flipkart.com/).

Fakekart's features mostly do not work -- you can't log in, add items to the cart, or buy anything. But, the core online shopping experience still works: searching, filtering, and browsing items.

The data for this project is originally sourced from this [Kaggle dataset](https://www.kaggle.com/datasets/PromptCloudHQ/flipkart-products) by PromptCloud. Thanks Flipkart, Kaggle and PromptCloud!

## Domain

These are the tables and columns in the database:

products
- id
- url
- name
- retail_price
- discounted_price
- flipkart_advantage
- rating
- overall_rating
- product_specifications

images
- id
- product_id
- url

categories
- id
- name

product_category
- product_id
- category_id

brands
- id
- name

product_brand
- product_id
- brand_id

## Starter Code

Fakekart uses Flask, Sqlite3, and [TailwindCSS](https://tailwindcss.com/).

- The application logic is in `app.py`
- The code for managing the database of products is in the `/products` folder.
- The templates are in `/templates`, with some shared components in `templates/shared`
- Static files like images and stylesheets are in `static`

Start the application in debug mode by running:

```sh
flask --debug run
```

and open [127.0.0.1:5000](http://127.0.0.1:5000) to view the application.

There are three routes that `app.py` serves:
- `'/'` is the index route, and it shows a landing page
- `'/products/<product_id>'` shows an individual product
- `'/search'` is a search results page

You should click through all of the pages to see how they currently behave. You'll be adding functionality to the search route and the search results page.

### Tailwind and NPM

This app uses [TailwindCSS](https://tailwindcss.com/) for styling.

The styles are pre-built in `static/styles.css`, so you should not need npm or to install anything to complete the project.

However, if you want to rebuild the styles, or if you want to edit the styles using tailwind, here's how to get started:

```sh
npm install # install the tailwind dependencies
npm run watch-styles # watch and rebuild the styles when files change
```

## Your Task

Right now, the search feature can filter by the name of the item, a min and max price, and by brands. It can use the default sort, or it can sort by ratings.

Your task is to add the missing search filters and sorts:
- add filter for items that are flipkart assured
- add filter for ratings (checkboxes)
- add filter for categories
- add sorting by price low-high and high-low
- add sorting by discount

## TODO
- get search to work
  - brand and category search
- styling / tailwind
- add links to category and brand searches
- if there is a brand or category search, show something at the top of the search results
