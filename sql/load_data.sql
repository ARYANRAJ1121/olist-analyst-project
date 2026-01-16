-- Load Olist raw CSV data into PostgreSQL
-- Assumes tables already created via schema.sql

-- Customers
COPY customers
FROM '/path/to/data/raw/olist_customers_dataset.csv'
DELIMITER ','
CSV HEADER;

-- Orders
COPY orders
FROM '/path/to/data/raw/olist_orders_dataset.csv'
DELIMITER ','
CSV HEADER;

-- Order Items
COPY order_items
FROM '/path/to/data/raw/olist_order_items_dataset.csv'
DELIMITER ','
CSV HEADER;

-- Payments
COPY payments
FROM '/path/to/data/raw/olist_order_payments_dataset.csv'
DELIMITER ','
CSV HEADER;

-- Products
COPY products
FROM '/path/to/data/raw/olist_products_dataset.csv'
DELIMITER ','
CSV HEADER;

-- Sellers
COPY sellers
FROM '/path/to/data/raw/olist_sellers_dataset.csv'
DELIMITER ','
CSV HEADER;

-- Reviews
COPY reviews
FROM '/path/to/data/raw/olist_order_reviews_dataset.csv'
DELIMITER ','
CSV HEADER;

-- Geolocation
COPY geolocation
FROM '/path/to/data/raw/olist_geolocation_dataset.csv'
DELIMITER ','
CSV HEADER;

-- Category Translation
COPY category_translation
FROM '/path/to/data/raw/product_category_name_translation.csv'
DELIMITER ','
CSV HEADER;
