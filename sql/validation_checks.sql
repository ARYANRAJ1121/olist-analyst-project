-- Data validation and sanity checks for Olist dataset

-- Row counts
SELECT 'customers' AS table_name, COUNT(*) FROM customers;
SELECT 'orders' AS table_name, COUNT(*) FROM orders;
SELECT 'order_items' AS table_name, COUNT(*) FROM order_items;
SELECT 'payments' AS table_name, COUNT(*) FROM payments;
SELECT 'products' AS table_name, COUNT(*) FROM products;
SELECT 'sellers' AS table_name, COUNT(*) FROM sellers;
SELECT 'reviews' AS table_name, COUNT(*) FROM reviews;

-- Check primary key uniqueness
SELECT customer_id, COUNT(*) 
FROM customers 
GROUP BY customer_id 
HAVING COUNT(*) > 1;

SELECT order_id, COUNT(*) 
FROM orders 
GROUP BY order_id 
HAVING COUNT(*) > 1;

-- Check missing critical fields
SELECT COUNT(*) AS missing_customer_ids
FROM orders
WHERE customer_id IS NULL;

SELECT COUNT(*) AS missing_order_dates
FROM orders
WHERE order_purchase_timestamp IS NULL;

-- Check negative or zero values
SELECT COUNT(*) AS invalid_prices
FROM order_items
WHERE price <= 0;

SELECT COUNT(*) AS invalid_payments
FROM payments
WHERE payment_value <= 0;
