import sqlite3
from sqlalchemy import create_engine, inspect
import json

db_url = "sqlite:///amazon.db"
engine = create_engine(db_url)
inspector = inspect(engine)

# Step 1: Extract Schema
def get_database_schema():
    """Extract complete database schema for context"""
    schema = {}
    for table in inspector.get_table_names():
        columns = inspector.get_columns(table)
        schema[table] = [
            {
                "name": col["name"],
                "type": str(col["type"]),
            }
            for col in columns
        ]
    return schema

schema = get_database_schema()
print("[SCHEMA] Database Schema loaded successfully")

# Step 2: Text to SQL (Demo - hardcoded examples)
def text_to_sql(user_query: str) -> str:
    """Convert natural language to SQL - DEMO VERSION with hardcoded queries"""

    queries = {
        "mumbai": "SELECT * FROM customers WHERE city = 'Mumbai'",
        "delhi": "SELECT * FROM customers WHERE city = 'Delhi'",
        "customers": "SELECT * FROM customers",
        "products": "SELECT * FROM products",
        "orders": "SELECT * FROM orders",
        "total sales": "SELECT category, SUM(price) as total FROM products GROUP BY category",
        "category": "SELECT category, COUNT(*) as count FROM products GROUP BY category",
        "expensive": "SELECT * FROM products WHERE price > 5000 ORDER BY price DESC",
        "cheap": "SELECT * FROM products WHERE price < 1000 ORDER BY price ASC",
        "order details": "SELECT o.order_id, c.name, p.name as product, oi.quantity FROM orders o JOIN customers c ON o.customer_id = c.customer_id JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id"
    }

    query_lower = user_query.lower()
    for keyword, sql in queries.items():
        if keyword in query_lower:
            return sql

    return "SELECT * FROM customers LIMIT 5"

# Step 3: Execute SQL and return results
def execute_query(sql_query: str):
    """Execute SQL query and return results"""
    try:
        conn = sqlite3.connect("amazon.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()

        if results and cursor.description:
            columns = [description[0] for description in cursor.description]
            data = [dict(row) for row in results]
            conn.close()
            return {"success": True, "columns": columns, "data": data}
        else:
            conn.close()
            return {"success": True, "columns": [], "data": []}
    except Exception as e:
        conn.close()
        return {"success": False, "error": str(e)}

# Main function to process user query
def analyze_data(user_query: str):
    """Main function that processes user query end-to-end"""
    print(f"\n[QUERY] User Query: {user_query}")

    # Convert text to SQL
    print("[CONVERTING] Converting to SQL (DEMO)...")
    sql_query = text_to_sql(user_query)
    print(f"[SUCCESS] Generated SQL: {sql_query}")

    # Execute query
    print("[EXECUTING] Executing query...")
    result = execute_query(sql_query)

    if result["success"]:
        print(f"[RESULTS] Results: {len(result['data'])} rows found")
        return sql_query, result
    else:
        print(f"[ERROR] Error: {result['error']}")
        return sql_query, result

if __name__ == "__main__":
    print("[INFO] DEMO MODE - No Ollama required!")
    print("[INFO] Try these queries:")
    print("[INFO] - 'Show customers from Mumbai'")
    print("[INFO] - 'Total sales by category'")
    print("[INFO] - 'Expensive products'")
    print()
    print("[INFO] To use the real AI version:")
    print("[INFO] 1. Install Ollama from ollama.ai")
    print("[INFO] 2. Run: ollama serve")
    print("[INFO] 3. Run: ollama pull deepseek-r1:8b")
    print("[INFO] 4. Change streamlit_app.py to import from main (not main_demo)")
    print()
    print("[INFO] Testing with a sample query...")
    try:
        test_query = "Show me customers from Mumbai"
        sql, results = analyze_data(test_query)
        print(f"[SUCCESS] Query completed")
        if results["success"]:
            print(f"[RESULTS] Found {len(results['data'])} rows")
    except Exception as e:
        print(f"[ERROR] {str(e)[:100]}")
