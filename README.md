# Product Pages

Relational databases are very common for E-commerce. In this project, you'll practice working with related data in multiple tables, adding features to a product pages website.

## Domain

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

## Your Task

Add features to search:
- currently filtered by like, price, brands
- current sorts: default (relevance), ratings
- add filter for flipkart assured
- add filter for ratings (checkboxes)
- add filter for categories
- add sorting by price low-high and high-low
- add sorting by discount

## Instructions

## Data

The data for this project is originally sourced from this [Kaggle dataset](https://www.kaggle.com/datasets/PromptCloudHQ/flipkart-products) by PromptCloud. Thanks Kaggle and PromptCloud!
