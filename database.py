import pyodbc
from typing import List, Dict, Any

# SQL Server Connection Configuration
SQL_SERVER_CONFIG = {
    "DRIVER": "ODBC Driver 18 for SQL Server",
    "SERVER": "DESKTOP-R733JC2\\SQLEXPRESS",
    "DATABASE": "master",
    "Trusted_Connection": "yes",
    "TrustServerCertificate": "yes",
}


def get_sql_server_connection():
    """Create and return a SQL Server connection"""
    conn_str = ";".join([f"{k}={v}" for k, v in SQL_SERVER_CONFIG.items()])
    return pyodbc.connect(conn_str)


def list_databases() -> List[str]:
    """List all databases in the SQL Server"""
    conn = get_sql_server_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.databases")
        databases = [row[0] for row in cursor.fetchall()]
        return databases
    finally:
        conn.close()


def execute_query(sql_query: str, database: str = "master") -> Dict[str, Any]:
    """Execute SQL query on SQL Server and return results"""
    if not sql_query.strip():
        return {"success": False, "error": "Empty SQL query"}

    conn = None
    try:
        config = SQL_SERVER_CONFIG.copy()
        config["DATABASE"] = database
        conn_str = ";".join([f"{k}={v}" for k, v in config.items()])
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute(sql_query)
        results = cursor.fetchall()

        if results and cursor.description:
            columns = [desc[0] for desc in cursor.description]
            data = [dict(zip(columns, row)) for row in results]
            return {"success": True, "columns": columns, "data": data}
        else:
            return {"success": True, "columns": [], "data": []}

    except pyodbc.Error as e:
        return {"success": False, "error": f"SQL Error: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    # Test the connection
    databases = list_databases()
    print("Available databases:")
    for db in databases:
        print(f"  - {db}")