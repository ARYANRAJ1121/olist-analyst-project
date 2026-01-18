-- =====================================================
-- Statistical Analysis: Churned vs Retained Customers
-- =====================================================

-- 1. Summary statistics by churn status
SELECT
    is_churned,
    COUNT(*) AS customers,
    ROUND(AVG(total_orders), 2) AS avg_orders,
    ROUND(AVG(total_revenue), 2) AS avg_revenue,
    ROUND(AVG(avg_order_value), 2) AS avg_aov,
    ROUND(AVG(days_since_last_order), 2) AS avg_days_since_last_order
FROM churn_features
GROUP BY is_churned;


-- 2. Distribution check (median values)
SELECT
    is_churned,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_orders) AS median_orders,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_revenue) AS median_revenue,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY days_since_last_order) AS median_recency
FROM churn_features
GROUP BY is_churned;


-- 3. Churn rate by order frequency bucket
SELECT
    CASE
        WHEN total_orders = 1 THEN '1 order'
        WHEN total_orders BETWEEN 2 AND 3 THEN '2-3 orders'
        WHEN total_orders BETWEEN 4 AND 6 THEN '4-6 orders'
        ELSE '7+ orders'
    END AS order_bucket,
    ROUND(AVG(is_churned::INT), 3) AS churn_rate,
    COUNT(*) AS customers
FROM churn_features
GROUP BY 1
ORDER BY 1;


-- 4. Churn rate by revenue bucket
SELECT
    CASE
        WHEN total_revenue < 100 THEN '<100'
        WHEN total_revenue BETWEEN 100 AND 500 THEN '100-500'
        WHEN total_revenue BETWEEN 500 AND 1000 THEN '500-1000'
        ELSE '1000+'
    END AS revenue_bucket,
    ROUND(AVG(is_churned::INT), 3) AS churn_rate,
    COUNT(*) AS customers
FROM churn_features
GROUP BY 1
ORDER BY 1;
