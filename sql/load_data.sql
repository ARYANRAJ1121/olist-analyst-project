-- Load Olist raw CSV data into PostgreSQL
-- Assumes tables already created via schema.sql
-- NOTE: Update the paths below to match your local data directory

-- @block Load customers
COPY customers
FROM 'C:/Users/Aryan Raj/OneDrive/Desktop/olist-analyst-project/data/raw/olist_customers_dataset.csv'
DELIMITER ','
CSV HEADER;

-- @block Load orders
COPY orders
FROM 'C:/Users/Aryan Raj/OneDrive/Desktop/olist-analyst-project/data/raw/olist_orders_dataset.csv'
DELIMITER ','
CSV HEADER;

-- @block Load order_items
COPY order_items
FROM 'C:/Users/Aryan Raj/OneDrive/Desktop/olist-analyst-project/data/raw/olist_order_items_dataset.csv'
DELIMITER ','
CSV HEADER;

-- @block Load payments
COPY payments
FROM 'C:/Users/Aryan Raj/OneDrive/Desktop/olist-analyst-project/data/raw/olist_order_payments_dataset.csv'
DELIMITER ','
CSV HEADER;

-- @block Load products
COPY products
FROM 'C:/Users/Aryan Raj/OneDrive/Desktop/olist-analyst-project/data/raw/olist_products_dataset.csv'
DELIMITER ','
CSV HEADER;

-- @block Load sellers
COPY sellers
FROM 'C:/Users/Aryan Raj/OneDrive/Desktop/olist-analyst-project/data/raw/olist_sellers_dataset.csv'
DELIMITER ','
CSV HEADER;

-- @block Load reviews
COPY reviews
FROM 'C:/Users/Aryan Raj/OneDrive/Desktop/olist-analyst-project/data/raw/olist_order_reviews_dataset.csv'
DELIMITER ','
CSV HEADER;

-- @block Load geolocation
COPY geolocation
FROM 'C:/Users/Aryan Raj/OneDrive/Desktop/olist-analyst-project/data/raw/olist_geolocation_dataset.csv'
DELIMITER ','
CSV HEADER;

-- @block Load category_translation
COPY category_translation
FROM 'C:/Users/Aryan Raj/OneDrive/Desktop/olist-analyst-project/data/raw/product_category_name_translation.csv'
DELIMITER ','
CSV HEADER;
