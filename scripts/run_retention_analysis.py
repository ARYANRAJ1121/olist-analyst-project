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

print("Tables loaded successfully")




retention_query = """
WITH customer_orders AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS total_orders
    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN total_orders > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(
        SUM(CASE WHEN total_orders > 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*),
        3
    ) AS repeat_purchase_rate
FROM customer_orders;
"""

df_retention = con.execute(retention_query).df()

print("\nRetention Metrics (Corrected):")
print(df_retention)


output_path = os.path.join(OUTPUT_DIR, "retention_metrics.csv")
df_retention.to_csv(output_path, index=False)

print(f"\nRetention metrics saved at: {output_path}")
