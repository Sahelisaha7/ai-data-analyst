"""Load CSV data into SQLite database"""
import sqlite3
import csv
from pathlib import Path

def create_database():
    """Create SQLite database and tables"""
    print("\n" + "="*60)
    print("LOADING DATA INTO DATABASE")
    print("="*60 + "\n")

    conn = sqlite3.connect("amazon.db")
    cursor = conn.cursor()

    # Drop existing tables (for fresh start)
    print("[1/5] Creating tables...")
    cursor.execute("DROP TABLE IF EXISTS order_items")
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS customers")

    # Create customers table
    cursor.execute("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE,
            city TEXT,
            phone TEXT,
            join_date DATE
        )
    """)

    # Create products table
    cursor.execute("""
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            price REAL,
            stock INTEGER,
            description TEXT
        )
    """)

    # Create orders table
    cursor.execute("""
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date DATE,
            total_amount REAL,
            status TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)

    # Create order_items table
    cursor.execute("""
        CREATE TABLE order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER,
            unit_price REAL,
            total_price REAL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

    conn.commit()
    print("[1/5] Tables created successfully\n")

    # Load customers
    print("[2/5] Loading customers...")
    load_csv_to_table(conn, "customers.csv", "customers")

    # Load products
    print("[3/5] Loading products...")
    load_csv_to_table(conn, "products.csv", "products")

    # Load orders
    print("[4/5] Loading orders...")
    load_csv_to_table(conn, "orders.csv", "orders")

    # Load order items
    print("[5/5] Loading order items...")
    load_csv_to_table(conn, "order_items.csv", "order_items")

    conn.close()

    print("\n" + "="*60)
    print("DATA LOADING COMPLETE!")
    print("="*60)
    print("\nDatabase: amazon.db")
    print("Tables created: customers, products, orders, order_items\n")

def load_csv_to_table(conn, csv_file, table_name):
    """Load CSV file into database table"""
    if not Path(csv_file).exists():
        print(f"ERROR: {csv_file} not found!")
        return

    cursor = conn.cursor()
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        if rows:
            columns = rows[0].keys()
            placeholders = ", ".join(["?" for _ in columns])
            insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

            for row in rows:
                values = tuple(row.values())
                try:
                    cursor.execute(insert_query, values)
                except Exception as e:
                    print(f"Error inserting row: {e}")

            conn.commit()
            row_count = cursor.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            print(f"  [OK] {table_name}: {row_count} rows loaded")

if __name__ == "__main__":
    create_database()
