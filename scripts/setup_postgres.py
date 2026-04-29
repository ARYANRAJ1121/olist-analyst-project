"""
Setup PostgreSQL database for the Olist project.

Run this ONCE to:
1. Create the 'olist' database (if it doesn't exist)
2. Create all tables from schema.sql
3. Load all CSV data into the tables
4. Create indexes for query performance

Usage:
    python scripts/setup_postgres.py

Prerequisites:
    - PostgreSQL installed and running
    - pip install psycopg2-binary
"""

import os
import sys

try:
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
except ImportError:
    print("❌ psycopg2 not installed. Run: pip install psycopg2-binary")
    sys.exit(1)

# ============================================================
# CONFIGURATION — Update these if your PostgreSQL setup differs
# ============================================================
PG_HOST = "localhost"
PG_PORT = 5432
PG_USER = "postgres"
PG_PASSWORD = input("Enter your PostgreSQL password for user 'postgres': ").strip()
DB_NAME = "olist"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
SQL_DIR = os.path.join(BASE_DIR, "sql")


def create_database():
    """Create the 'olist' database if it doesn't exist."""
    print(f"\n📦 Connecting to PostgreSQL at {PG_HOST}:{PG_PORT}...")
    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT,
        user=PG_USER, password=PG_PASSWORD,
        dbname="postgres"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Check if database exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    if cur.fetchone():
        print(f"  ✅ Database '{DB_NAME}' already exists. Dropping and recreating...")
        # Terminate existing connections
        cur.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{DB_NAME}'
              AND pid <> pg_backend_pid()
        """)
        cur.execute(f'DROP DATABASE "{DB_NAME}"')

    cur.execute(f'CREATE DATABASE "{DB_NAME}"')
    print(f"  ✅ Database '{DB_NAME}' created.")

    cur.close()
    conn.close()


def get_connection():
    """Get a connection to the olist database."""
    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT,
        user=PG_USER, password=PG_PASSWORD,
        dbname=DB_NAME
    )


def create_tables(conn):
    """Create tables (schema only, no indexes yet)."""
    print("\n🏗️  Creating tables...")
    cur = conn.cursor()

    # Create tables
    cur.execute("""
        CREATE TABLE customers (
            customer_id VARCHAR PRIMARY KEY,
            customer_unique_id VARCHAR,
            customer_zip_code_prefix INTEGER,
            customer_city VARCHAR,
            customer_state VARCHAR
        );

        CREATE TABLE orders (
            order_id VARCHAR PRIMARY KEY,
            customer_id VARCHAR REFERENCES customers(customer_id),
            order_status VARCHAR,
            order_purchase_timestamp TIMESTAMP,
            order_approved_at TIMESTAMP,
            order_delivered_carrier_date TIMESTAMP,
            order_delivered_customer_date TIMESTAMP,
            order_estimated_delivery_date TIMESTAMP
        );

        CREATE TABLE order_items (
            order_id VARCHAR REFERENCES orders(order_id),
            order_item_id INTEGER,
            product_id VARCHAR,
            seller_id VARCHAR,
            shipping_limit_date TIMESTAMP,
            price NUMERIC,
            freight_value NUMERIC,
            PRIMARY KEY (order_id, order_item_id)
        );

        CREATE TABLE payments (
            order_id VARCHAR REFERENCES orders(order_id),
            payment_sequential INTEGER,
            payment_type VARCHAR,
            payment_installments INTEGER,
            payment_value NUMERIC
        );

        CREATE TABLE products (
            product_id VARCHAR PRIMARY KEY,
            product_category_name VARCHAR,
            product_weight_g INTEGER,
            product_length_cm INTEGER,
            product_height_cm INTEGER,
            product_width_cm INTEGER
        );

        CREATE TABLE sellers (
            seller_id VARCHAR PRIMARY KEY,
            seller_zip_code_prefix INTEGER,
            seller_city VARCHAR,
            seller_state VARCHAR
        );

        CREATE TABLE reviews (
            id SERIAL PRIMARY KEY,
            review_id VARCHAR,
            order_id VARCHAR REFERENCES orders(order_id),
            review_score INTEGER,
            review_comment_title TEXT,
            review_comment_message TEXT,
            review_creation_date TIMESTAMP,
            review_answer_timestamp TIMESTAMP
        );

        CREATE TABLE geolocation (
            geolocation_zip_code_prefix INTEGER,
            geolocation_lat NUMERIC,
            geolocation_lng NUMERIC,
            geolocation_city VARCHAR,
            geolocation_state VARCHAR
        );

        CREATE TABLE category_translation (
            product_category_name VARCHAR PRIMARY KEY,
            product_category_name_english VARCHAR
        );
    """)
    conn.commit()
    cur.close()
    print("  ✅ All tables created.")


def load_csv_to_table(conn, table_name, csv_filename, columns=None):
    """Load a CSV file into a PostgreSQL table using COPY."""
    csv_path = os.path.join(DATA_DIR, csv_filename)

    if not os.path.exists(csv_path):
        print(f"  ⚠️  {csv_filename} not found — skipped")
        return 0

    cur = conn.cursor()

    # If columns specified (for tables with auto-generated PK), use them
    if columns:
        col_list = ", ".join(columns)
        copy_sql = f"COPY {table_name}({col_list}) FROM STDIN WITH CSV HEADER DELIMITER ','"
    else:
        copy_sql = f"COPY {table_name} FROM STDIN WITH CSV HEADER DELIMITER ','"

    with open(csv_path, "r", encoding="utf-8") as f:
        cur.copy_expert(copy_sql, f)

    conn.commit()

    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cur.fetchone()[0]
    cur.close()

    print(f"  ✅ {table_name}: {count:,} rows loaded")
    return count


def create_indexes(conn):
    """Create indexes for query performance."""
    print("\n⚡ Creating indexes for fast queries...")
    cur = conn.cursor()

    indexes = [
        "CREATE INDEX idx_orders_customer_id ON orders(customer_id)",
        "CREATE INDEX idx_orders_status ON orders(order_status)",
        "CREATE INDEX idx_orders_purchase_ts ON orders(order_purchase_timestamp)",
        "CREATE INDEX idx_orders_customer_status ON orders(customer_id, order_status)",
        "CREATE INDEX idx_payments_order_id ON payments(order_id)",
        "CREATE INDEX idx_order_items_order_id ON order_items(order_id)",
        "CREATE INDEX idx_reviews_order_id ON reviews(order_id)",
    ]

    for idx_sql in indexes:
        idx_name = idx_sql.split("INDEX ")[1].split(" ON")[0]
        cur.execute(idx_sql)
        print(f"  ✅ {idx_name}")

    conn.commit()
    cur.close()


def load_all_data(conn):
    """Load all CSV files into their respective tables."""
    print("\n📥 Loading CSV data into PostgreSQL...")

    # Order matters due to foreign key constraints
    # reviews has SERIAL PK, so we must specify column names
    review_columns = [
        "review_id", "order_id", "review_score",
        "review_comment_title", "review_comment_message",
        "review_creation_date", "review_answer_timestamp"
    ]

    tables = [
        ("customers", "olist_customers_dataset.csv", None),
        ("orders", "olist_orders_dataset.csv", None),
        ("order_items", "olist_order_items_dataset.csv", None),
        ("payments", "olist_order_payments_dataset.csv", None),
        ("products", "olist_products_dataset.csv", None),
        ("sellers", "olist_sellers_dataset.csv", None),
        ("reviews", "olist_order_reviews_dataset.csv", review_columns),
        ("geolocation", "olist_geolocation_dataset.csv", None),
        ("category_translation", "product_category_name_translation.csv", None),
    ]

    total_rows = 0
    for table_name, csv_file, columns in tables:
        try:
            rows = load_csv_to_table(conn, table_name, csv_file, columns)
            total_rows += rows
        except Exception as e:
            print(f"  ❌ Error loading {table_name}: {e}")
            conn.rollback()

    return total_rows


def verify_database(conn):
    """Print a summary of the database."""
    print("\n📊 Database Summary:")
    cur = conn.cursor()

    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    tables = cur.fetchall()

    for (table_name,) in tables:
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cur.fetchone()[0]
        print(f"   {table_name}: {count:,} rows")

    cur.close()


def main():
    # Step 1: Create database (fresh)
    create_database()

    # Step 2: Connect
    conn = get_connection()
    print(f"  ✅ Connected to '{DB_NAME}' database.")

    try:
        # Step 3: Create tables
        create_tables(conn)

        # Step 4: Load data
        total = load_all_data(conn)
        print(f"\n  📚 Total rows loaded: {total:,}")

        # Step 5: Create indexes
        create_indexes(conn)

        # Step 6: Verify
        verify_database(conn)

    finally:
        conn.close()

    print(f"\n🎉 Done! PostgreSQL database '{DB_NAME}' is ready.")
    print("   Open SQLTools → Connect to 'Olist PostgreSQL' → Run queries!")


if __name__ == "__main__":
    main()
