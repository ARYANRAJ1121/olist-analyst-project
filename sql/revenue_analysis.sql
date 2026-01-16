-- =====================================================
-- Revenue & Growth Analysis
-- Business Question:
-- How is revenue evolving over time, and what drives it?
-- =====================================================

-- 1. Monthly revenue trend
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
    ROUND(SUM(p.payment_value), 2) AS monthly_revenue
FROM orders o
JOIN payments p
    ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY 1
ORDER BY 1;


-- 2. Monthly order volume
SELECT
    DATE_TRUNC('month', order_purchase_timestamp) AS month,
    COUNT(DISTINCT order_id) AS total_orders
FROM orders
WHERE order_status = 'delivered'
GROUP BY 1
ORDER BY 1;


-- 3. Average Order Value (AOV) by month
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
    ROUND(SUM(p.payment_value) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
FROM orders o
JOIN payments p
    ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY 1
ORDER BY 1;


-- 4. Monthly active customers
SELECT
    DATE_TRUNC('month', order_purchase_timestamp) AS month,
    COUNT(DISTINCT customer_id) AS active_customers
FROM orders
WHERE order_status = 'delivered'
GROUP BY 1
ORDER BY 1;


-- 5. Revenue per active customer (monetization quality)
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
    ROUND(SUM(p.payment_value) / COUNT(DISTINCT o.customer_id), 2) AS revenue_per_customer
FROM orders o
JOIN payments p
    ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY 1
ORDER BY 1;
