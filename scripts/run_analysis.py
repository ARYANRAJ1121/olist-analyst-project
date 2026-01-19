import duckdb
import pandas as pd
import os

# =============================
# PATH SETUP
# =============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =============================
# CONNECT TO DUCKDB
# =============================
con = duckdb.connect()
print("Connected to DuckDB")

# =============================
# LOAD REQUIRED TABLES
# =============================
print("Loading orders table...")
con.execute(f"""
    CREATE TABLE orders AS
    SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, "olist_orders_dataset.csv")}');
""")

print("Loading payments table...")
con.execute(f"""
    CREATE TABLE payments AS
    SELECT * FROM read_csv_auto('{os.path.join(DATA_DIR, "olist_order_payments_dataset.csv")}');
""")

print("Tables loaded successfully")

# =============================
# REVENUE ANALYSIS
# =============================
revenue_query = """
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
    ROUND(SUM(p.payment_value), 2) AS revenue
FROM orders o
JOIN payments p
    ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY 1
ORDER BY 1;
"""

df_revenue = con.execute(revenue_query).df()

print("\nMonthly Revenue (Top 5 Rows):")
print(df_revenue.head())

# =============================
# SAVE OUTPUT
# =============================
output_path = os.path.join(OUTPUT_DIR, "monthly_revenue.csv")
df_revenue.to_csv(output_path, index=False)

print(f"\nRevenue output saved at: {output_path}")
