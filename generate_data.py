"""Generate realistic sample data for the AI Data Analyst project"""
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
NUM_CUSTOMERS = 1000
NUM_PRODUCTS = 500
NUM_ORDERS = 5000
ITEMS_PER_ORDER = 2

# Sample data
FIRST_NAMES = ["John", "Emma", "Michael", "Sophia", "David", "Olivia", "James", "Ava", "Robert", "Isabella"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
CITIES = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow"]
PRODUCT_NAMES = [
    "Laptop", "Smartphone", "Tablet", "Headphones", "Smart Watch",
    "Monitor", "Keyboard", "Mouse", "Webcam", "Speaker",
    "USB Cable", "Power Bank", "Phone Case", "Screen Protector", "Charger",
    "Camera", "Microphone", "Router", "External HDD", "RAM"
]
CATEGORIES = ["Electronics", "Accessories", "Computers", "Networking", "Storage"]

def generate_customers(num_customers):
    """Generate customer CSV"""
    print(f"Generating {num_customers} customers...")
    customers = []

    for i in range(1, num_customers + 1):
        customers.append({
            "customer_id": i,
            "first_name": random.choice(FIRST_NAMES),
            "last_name": random.choice(LAST_NAMES),
            "email": f"customer{i}@example.com",
            "city": random.choice(CITIES),
            "phone": f"9{random.randint(100000000, 999999999)}",
            "join_date": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
        })

    with open("customers.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=customers[0].keys())
        writer.writeheader()
        writer.writerows(customers)

    print(f"[OK] Created customers.csv with {num_customers} rows")
    return customers

def generate_products(num_products):
    """Generate product CSV"""
    print(f"Generating {num_products} products...")
    products = []

    for i in range(1, num_products + 1):
        products.append({
            "product_id": i,
            "product_name": f"{random.choice(PRODUCT_NAMES)} {i}",
            "category": random.choice(CATEGORIES),
            "price": round(random.uniform(500, 50000), 2),
            "stock": random.randint(0, 1000),
            "description": f"Quality product {i}"
        })

    with open("products.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products)

    print(f"[OK] Created products.csv with {num_products} rows")
    return products

def generate_orders(num_orders, num_customers):
    """Generate order CSV"""
    print(f"Generating {num_orders} orders...")
    orders = []

    for i in range(1, num_orders + 1):
        order_date = datetime.now() - timedelta(days=random.randint(1, 365))
        orders.append({
            "order_id": i,
            "customer_id": random.randint(1, num_customers),
            "order_date": order_date.strftime("%Y-%m-%d"),
            "total_amount": round(random.uniform(1000, 100000), 2),
            "status": random.choice(["Pending", "Processing", "Shipped", "Delivered", "Cancelled"])
        })

    with open("orders.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=orders[0].keys())
        writer.writeheader()
        writer.writerows(orders)

    print(f"[OK] Created orders.csv with {num_orders} rows")
    return orders

def generate_order_items(num_orders, num_products):
    """Generate order items CSV"""
    print(f"Generating order items (~{num_orders * ITEMS_PER_ORDER} rows)...")
    order_items = []
    item_id = 1

    for order_id in range(1, num_orders + 1):
        num_items = random.randint(1, ITEMS_PER_ORDER * 2)
        for _ in range(num_items):
            quantity = random.randint(1, 5)
            price = round(random.uniform(500, 50000), 2)
            order_items.append({
                "item_id": item_id,
                "order_id": order_id,
                "product_id": random.randint(1, num_products),
                "quantity": quantity,
                "unit_price": price,
                "total_price": round(quantity * price, 2)
            })
            item_id += 1

    with open("order_items.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=order_items[0].keys())
        writer.writeheader()
        writer.writerows(order_items)

    print(f"[OK] Created order_items.csv with {len(order_items)} rows")
    return order_items

def main():
    """Generate all CSV files"""
    print("\n" + "="*60)
    print("GENERATING SAMPLE DATA")
    print("="*60 + "\n")

    generate_customers(NUM_CUSTOMERS)
    generate_products(NUM_PRODUCTS)
    generate_orders(NUM_ORDERS, NUM_CUSTOMERS)
    generate_order_items(NUM_ORDERS, NUM_PRODUCTS)

    print("\n" + "="*60)
    print("DATA GENERATION COMPLETE!")
    print("="*60)
    print(f"\nGenerated CSV files:")
    print(f"  - customers.csv ({NUM_CUSTOMERS} rows)")
    print(f"  - products.csv ({NUM_PRODUCTS} rows)")
    print(f"  - orders.csv ({NUM_ORDERS} rows)")
    print(f"  - order_items.csv (~{NUM_ORDERS * ITEMS_PER_ORDER} rows)")
    print(f"\nTotal data points: ~{NUM_CUSTOMERS + NUM_PRODUCTS + NUM_ORDERS + (NUM_ORDERS * ITEMS_PER_ORDER):,}\n")

if __name__ == "__main__":
    main()
