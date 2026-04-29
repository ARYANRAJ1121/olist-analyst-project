"""
Setup persistent DuckDB database for SQLTools in VS Code.

Run this ONCE to create olist.duckdb with all tables loaded from CSV files.
Then connect to it via SQLTools to run any .sql file interactively.
"""

import duckdb
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
DB_PATH = os.path.join(BASE_DIR, "olist.duckdb")

# Remove old DB if exists (fresh start)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print(f"🗑️  Removed old database: {DB_PATH}")

# Create persistent DuckDB database
con = duckdb.connect(DB_PATH)
print(f"📦 Creating persistent DuckDB at: {DB_PATH}\n")

# ============================================================
# Load all tables from CSV files
# ============================================================

tables = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}

for table_name, csv_file in tables.items():
    csv_path = os.path.join(DATA_DIR, csv_file)
    if os.path.exists(csv_path):
        con.execute(f"""
            CREATE TABLE {table_name} AS
            SELECT * FROM read_csv_auto('{csv_path.replace(os.sep, '/')}');
        """)
        count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"  ✅ {table_name}: {count:,} rows loaded")
    else:
        print(f"  ⚠️  {csv_file} not found — skipped")

# ============================================================
# Verify
# ============================================================
print("\n📊 Database summary:")
tables_info = con.execute("SHOW TABLES").fetchall()
for (t,) in tables_info:
    count = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"   {t}: {count:,} rows")

con.close()
print(f"\n🎉 Done! Database saved at: {DB_PATH}")
print("   Now open SQLTools in VS Code and connect to this file.")
