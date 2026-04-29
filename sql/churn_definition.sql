-- =====================================================
-- Churn Definition
-- Business Question:
-- Which customers have churned based on inactivity?
-- =====================================================

-- @block Define churn (90-day inactivity window)
WITH customer_last_order AS (
    SELECT
        customer_id,
        MAX(order_purchase_timestamp) AS last_order_date
    FROM orders
    WHERE order_status = 'delivered'
    GROUP BY customer_id
),

churn_flag AS (
    SELECT
        c.customer_id,
        c.last_order_date,
        CASE
            WHEN EXISTS (
                SELECT 1
                FROM orders o
                WHERE o.customer_id = c.customer_id
                  AND o.order_purchase_timestamp > c.last_order_date
                  AND o.order_purchase_timestamp <= c.last_order_date + INTERVAL '90 days'
            )
            THEN 0
            ELSE 1
        END AS is_churned
    FROM customer_last_order c
)

SELECT * FROM churn_flag;
