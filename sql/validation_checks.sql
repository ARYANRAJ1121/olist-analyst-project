-- Data validation and sanity checks for Olist dataset

-- @block Row counts
SELECT 'customers' AS table_name, COUNT(*) FROM customers
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'payments', COUNT(*) FROM payments
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'sellers', COUNT(*) FROM sellers
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews;

-- @block Check customer_id uniqueness
SELECT customer_id, COUNT(*) 
FROM customers 
GROUP BY customer_id 
HAVING COUNT(*) > 1;

-- @block Check order_id uniqueness
SELECT order_id, COUNT(*) 
FROM orders 
GROUP BY order_id 
HAVING COUNT(*) > 1;

-- @block Check missing critical fields
SELECT 
    COUNT(*) FILTER (WHERE customer_id IS NULL) AS missing_customer_ids,
    COUNT(*) FILTER (WHERE order_purchase_timestamp IS NULL) AS missing_order_dates
FROM orders;

-- @block Check invalid prices and payments
SELECT 
    (SELECT COUNT(*) FROM order_items WHERE price <= 0) AS invalid_prices,
    (SELECT COUNT(*) FROM payments WHERE payment_value <= 0) AS invalid_payments;




