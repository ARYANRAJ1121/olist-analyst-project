-- =====================================================
-- Churn Feature Table
-- One row per customer for churn analysis
-- =====================================================

WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS total_orders,
        MIN(order_purchase_timestamp) AS first_order_date,
        MAX(order_purchase_timestamp) AS last_order_date
    FROM orders
    WHERE order_status = 'delivered'
    GROUP BY customer_id
),

customer_revenue AS (
    SELECT
        o.customer_id,
        SUM(p.payment_value) AS total_revenue,
        AVG(p.payment_value) AS avg_order_value
    FROM orders o
    JOIN payments p
        ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY o.customer_id
),

customer_recency AS (
    SELECT
        customer_id,
        CURRENT_DATE - MAX(order_purchase_timestamp)::DATE AS days_since_last_order
    FROM orders
    WHERE order_status = 'delivered'
    GROUP BY customer_id
),

churn_labels AS (
    SELECT
        customer_id,
        is_churned
    FROM (
        -- reuse churn logic (90-day inactivity)
        SELECT
            c.customer_id,
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
        FROM (
            SELECT
                customer_id,
                MAX(order_purchase_timestamp) AS last_order_date
            FROM orders
            WHERE order_status = 'delivered'
            GROUP BY customer_id
        ) c
    ) x
)

SELECT
    co.customer_id,
    co.total_orders,
    cr.total_revenue,
    cr.avg_order_value,
    co.first_order_date,
    co.last_order_date,
    r.days_since_last_order,
    cl.is_churned
FROM customer_orders co
LEFT JOIN customer_revenue cr
    ON co.customer_id = cr.customer_id
LEFT JOIN customer_recency r
    ON co.customer_id = r.customer_id
LEFT JOIN churn_labels cl
    ON co.customer_id = cl.customer_id;
