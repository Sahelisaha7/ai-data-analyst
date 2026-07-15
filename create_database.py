import sqlite3


# step1: create Dummy database

conn = sqlite3.connect('amazon.db')
cursor = conn.cursor()

# step2: create Tables
# tables: customer, orders, products, order_items

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
               customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
               email TEXT,
               city TEXT,
               join_date TEXT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    price REAL
)
    """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    order_date TEXT,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        subtotal REAL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
               )
               """)
# step3: Enter dummy data
# customer
customer = [
    ("Aarav Sharma", "aarav.sharma@example.com", "Kolkata", "2026-07-01"),
    ("Priya Das", "priya.das@example.com", "Mumbai", "2026-07-02"),
    ("Rohan Sen", "rohan.sen@example.com", "Delhi", "2026-07-03"),
    ("Sneha Gupta", "sneha.gupta@example.com", "Bengaluru", "2026-07-04"),
    ("Arjun Roy", "arjun.roy@example.com", "Hyderabad", "2026-07-05")
]
cursor.executemany("INSERT INTO customers (name, email, city, join_date) VALUES (?,?,?,?)", customer)


products = [
    ("Laptop", "Electronics", 65000.00),
    ("Wireless Mouse", "Electronics", 899.00),
    ("Office Chair", "Furniture", 5500.00),
    ("Water Bottle", "Home", 399.00),
    ("Notebook", "Stationery", 120.00)
   ]
cursor.executemany("INSERT INTO products (name, category, price) VALUES (?,?,?)", products)

# orders
orders = [
    (1, "2026-07-01", 65899.00),
    (2, "2026-07-02", 70399.00),
    (3, "2026-07-03", 5500.00),
    (4, "2026-07-04", 66399.00),
    (5, "2026-07-05", 1019.00)
]
cursor.executemany("INSERT INTO orders (customer_id, order_date, total_amount) VALUES (?,?,?)", orders)

# order_items
order_items = [
    (1, 1, 1, 65000.00),
    (2, 2, 1, 899.00),
    (3, 3, 2, 11000.00),
    (4, 4, 3, 1197.00),
    (5, 5, 1, 120.00)
]
cursor.executemany("INSERT INTO order_items (order_id, product_id, quantity, subtotal) VALUES (?,?,?,?)", order_items)

conn.commit()
conn.close()

print("Database 'amazon.db' created successfully with all dummy data!")
