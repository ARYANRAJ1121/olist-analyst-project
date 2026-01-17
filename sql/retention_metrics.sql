-- =====================================================
-- Customer Retention Metrics
-- Business Question:
-- How frequently do customers return and how strong is retention?
-- =====================================================

-- 1. Orders per customer
WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS total_orders
    FROM orders
    WHERE order_status = 'delivered'
    GROUP BY customer_id
),

-- 2. Repeat purchase rate
repeat_rate AS (
    SELECT
        COUNT(CASE WHEN total_orders > 1 THEN 1 END)::DECIMAL
        / COUNT(*) AS repeat_purchase_rate
    FROM customer_orders
)

SELECT * FROM repeat_rate;


-- 3. Average orders per customer
SELECT
    ROUND(AVG(total_orders), 2) AS avg_orders_per_customer
FROM customer_orders;


-- 4. Average time between orders (in days)
WITH ordered_events AS (
    SELECT
        customer_id,
        order_purchase_timestamp,
        LAG(order_purchase_timestamp) OVER (
            PARTITION BY customer_id
            ORDER BY order_purchase_timestamp
        ) AS previous_order_date
    FROM orders
    WHERE order_status = 'delivered'
),

time_between_orders AS (
    SELECT
        customer_id,
        order_purchase_timestamp - previous_order_date AS days_between
    FROM ordered_events
    WHERE previous_order_date IS NOT NULL
)

SELECT
    ROUND(AVG(days_between), 2) AS avg_days_between_orders
FROM time_between_orders;
