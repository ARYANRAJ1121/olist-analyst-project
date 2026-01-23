import duckdb
import pandas as pd
import os



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)


con = duckdb.connect()
print("Connected to DuckDB")


con.execute(f"""
CREATE TABLE orders AS
SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, "olist_orders_dataset.csv")}');
""")

con.execute(f"""
CREATE TABLE customers AS
SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, "olist_customers_dataset.csv")}');
""")

con.execute(f"""
CREATE TABLE payments AS
SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, "olist_order_payments_dataset.csv")}');
""")

print("Tables loaded")


dataset_end_date = con.execute("""
SELECT MAX(order_purchase_timestamp)::DATE FROM orders;
""").fetchone()[0]

print(f"Dataset end date: {dataset_end_date}")


churn_query = f"""
WITH customer_orders AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS total_orders,
        MIN(o.order_purchase_timestamp)::DATE AS first_order_date,
        MAX(o.order_purchase_timestamp)::DATE AS last_order_date
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
)

SELECT
    co.customer_unique_id,
    co.total_orders,
    cr.total_revenue,
    cr.avg_order_value,
    co.first_order_date,
    co.last_order_date,
    DATE '{dataset_end_date}' - co.last_order_date AS days_since_last_order,
    CASE
        WHEN DATE '{dataset_end_date}' - co.last_order_date > 90 THEN 1
        ELSE 0
    END AS is_churned
FROM customer_orders co
LEFT JOIN customer_revenue cr
    ON co.customer_unique_id = cr.customer_unique_id;
"""

df_churn = con.execute(churn_query).df()
print("\nChurn Feature Table Preview:")
print(df_churn.head())


output_path = os.path.join(OUTPUT_DIR, "churn_features_v2.csv")
df_churn.to_csv(output_path, index=False)

print(f"\nChurn features v2 saved at: {output_path}")

