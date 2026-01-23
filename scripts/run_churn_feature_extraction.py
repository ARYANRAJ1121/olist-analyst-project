import duckdb
import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

con = duckdb.connect()
print("Connected to DuckDB")


print("Loading orders...")
con.execute(f"""
    CREATE TABLE orders AS
    SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, "olist_orders_dataset.csv")}');
""")

print("Loading customers...")
con.execute(f"""
    CREATE TABLE customers AS
    SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, "olist_customers_dataset.csv")}');
""")

print("Loading payments...")
con.execute(f"""
    CREATE TABLE payments AS
    SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, "olist_order_payments_dataset.csv")}');
""")

print("Tables loaded successfully")


churn_query = """
WITH customer_orders AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS total_orders,
        MIN(o.order_purchase_timestamp) AS first_order_date,
        MAX(o.order_purchase_timestamp) AS last_order_date
    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),

customer_revenue AS (
    SELECT
        c.customer_unique_id,
        SUM(p.payment_value) AS total_revenue,
        AVG(p.payment_value) AS avg_order_value
    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id
    JOIN payments p
        ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),

churn_labels AS (
    SELECT
        customer_unique_id,
        CASE
            WHEN CURRENT_DATE - last_order_date::DATE > 90
            THEN 1
            ELSE 0
        END AS is_churned
    FROM customer_orders
)

SELECT
    co.customer_unique_id,
    co.total_orders,
    cr.total_revenue,
    cr.avg_order_value,
    co.first_order_date,
    co.last_order_date,
    (CURRENT_DATE - co.last_order_date::DATE) AS days_since_last_order,
    cl.is_churned
FROM customer_orders co
LEFT JOIN customer_revenue cr
    ON co.customer_unique_id = cr.customer_unique_id
LEFT JOIN churn_labels cl
    ON co.customer_unique_id = cl.customer_unique_id;
"""

df_churn = con.execute(churn_query).df()

print("\nChurn Feature Table Preview:")
print(df_churn.head())


output_path = os.path.join(OUTPUT_DIR, "churn_features.csv")
df_churn.to_csv(output_path, index=False)

print(f"\nChurn feature table saved at: {output_path}")
