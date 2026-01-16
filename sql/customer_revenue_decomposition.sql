-- =====================================================
-- Customer Revenue Decomposition
-- Business Question:
-- Is revenue driven by new customers or repeat customers?
-- =====================================================

-- 1. First purchase date per customer
WITH first_purchase AS (
    SELECT
        customer_id,
        MIN(order_purchase_timestamp) AS first_order_date
    FROM orders
    WHERE order_status = 'delivered'
    GROUP BY customer_id
),

-- 2. Tag each order as new or repeat
order_classification AS (
    SELECT
        o.order_id,
        o.customer_id,
        DATE_TRUNC('month', o.order_purchase_timestamp) AS order_month,
        CASE
            WHEN DATE_TRUNC('month', o.order_purchase_timestamp)
                 = DATE_TRUNC('month', f.first_order_date)
            THEN 'new_customer'
            ELSE 'repeat_customer'
        END AS customer_type
    FROM orders o
    JOIN first_purchase f
        ON o.customer_id = f.customer_id
    WHERE o.order_status = 'delivered'
)

-- 3. Monthly revenue by customer type
SELECT
    oc.order_month,
    oc.customer_type,
    ROUND(SUM(p.payment_value), 2) AS revenue
FROM order_classification oc
JOIN payments p
    ON oc.order_id = p.order_id
GROUP BY 1, 2
ORDER BY 1, 2;
