import json
import os
import sys
import re
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from dotenv import load_dotenv
from anthropic import Anthropic
import database

load_dotenv()


@dataclass
class Config:
    """Configuration management"""
    api_key: str
    database: str = "master"
    model: str = "claude-opus-4-1"

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Please set it in .env file:\n"
                "  ANTHROPIC_API_KEY=your-key-here"
            )
        db = os.getenv("SQL_DATABASE", "master")
        return cls(api_key=api_key, database=db)


class DatabaseManager:
    """Handle all database operations"""

    def __init__(self, db_name: str):
        self.db_name = db_name
        self._initialize()

    def _initialize(self):
        """Initialize database connection"""
        try:
            database.get_sql_server_connection().close()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to SQL Server: {e}")

    def get_schema(self) -> Dict[str, List[Dict[str, str]]]:
        """Extract complete database schema"""
        schema = {}
        try:
            query = """
            SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
            """
            result = database.execute_query(query, self.db_name)

            if not result["success"]:
                raise RuntimeError(f"Failed to get tables: {result['error']}")

            tables = [row["TABLE_NAME"] for row in result["data"]]

            for table in tables:
                col_query = f"""
                SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table}'
                """
                col_result = database.execute_query(col_query, self.db_name)

                if col_result["success"]:
                    schema[table] = [
                        {"name": col["COLUMN_NAME"], "type": col["DATA_TYPE"]}
                        for col in col_result["data"]
                    ]

            return schema
        except Exception as e:
            raise RuntimeError(f"Failed to extract schema: {e}")

    def execute_query(self, sql_query: str) -> Dict[str, Any]:
        """Execute SQL query and return results safely"""
        return database.execute_query(sql_query, self.db_name)


class SQLGenerator:
    """Handle natural language to SQL conversion using Claude"""

    def __init__(self, client: Anthropic, model: str, schema: Dict[str, Any]):
        self.client = client
        self.model = model
        self.schema = schema

    def generate(self, user_query: str) -> str:
        """Convert natural language query to SQL"""
        if not user_query.strip():
            raise ValueError("Query cannot be empty")

        schema_context = json.dumps(self.schema, indent=2)
        prompt = self._build_prompt(user_query, schema_context)

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            sql_query = message.content[0].text.strip()

            # Remove markdown code blocks - simple approach
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

            return sql_query

        except Exception as e:
            raise RuntimeError(f"Failed to generate SQL: {str(e)}")

    @staticmethod
    def _build_prompt(user_query: str, schema_context: str) -> str:
        """Build the prompt for SQL generation"""
        return f"""You are a SQL expert. Convert the user's natural language question into a valid SQL Server T-SQL query.

Database Schema:
{schema_context}

User Question: {user_query}

Rules:
- Return ONLY the SQL query, nothing else
- Use proper T-SQL syntax for SQL Server
- JOIN tables when needed
- Use aliases for clarity
- Ensure the query is valid SQL Server syntax
- Handle NULL values appropriately
- Use CAST() or CONVERT() for type conversions if needed

SQL Query:"""


class DataAnalyzer:
    """Main analyzer that orchestrates the entire process"""

    def __init__(self, config: Config):
        self.config = config
        self.client = Anthropic(api_key=config.api_key)
        self.db = DatabaseManager(config.database)
        self.schema = self.db.get_schema()
        self.sql_gen = SQLGenerator(self.client, config.model, self.schema)

    def analyze(self, user_query: str) -> Tuple[str, Dict[str, Any]]:
        """
        Analyze user query and return SQL and results

        Args:
            user_query: Natural language query from user

        Returns:
            Tuple of (generated_sql, results_dict)
        """
        if not user_query.strip():
            raise ValueError("Query cannot be empty")

        print(f"\n{'='*60}")
        print(f"[QUERY] {user_query}")
        print(f"{'='*60}")

        # Step 1: Convert to SQL
        print("[STEP 1] Converting natural language to SQL...")
        try:
            sql_query = self.sql_gen.generate(user_query)
            print(f"[STEP 1] Generated SQL:\n  {sql_query}\n")
        except Exception as e:
            print(f"[ERROR] Failed to generate SQL: {e}")
            raise

        # Step 2: Execute query
        print("[STEP 2] Executing SQL query...")
        result = self.db.execute_query(sql_query)

        if result["success"]:
            row_count = len(result["data"])
            print(f"[STEP 2] Query executed successfully: {row_count} rows found\n")
        else:
            print(f"[ERROR] Query execution failed: {result['error']}\n")

        return sql_query, result

    def display_results(self, sql_query: str, result: Dict[str, Any]):
        """Display results in a formatted way"""
        if not result["success"]:
            print(f"[ERROR] {result['error']}")
            return

        if not result["data"]:
            print("[SUCCESS] Query executed successfully but returned no results.")
            return

        print("[RESULTS]")
        print("-" * 60)

        # Display column headers
        if result["columns"]:
            print(" | ".join(result["columns"]))
            print("-" * 60)

        # Display data (limit to 10 rows for display)
        display_rows = result["data"][:10]
        for row in display_rows:
            values = [str(v)[:20] for v in row.values()]
            print(" | ".join(values))

        if len(result["data"]) > 10:
            print(f"... and {len(result['data']) - 10} more rows")

        print("-" * 60)
        print(f"Total: {len(result['data'])} rows\n")


def select_database() -> str:
    """List available databases and let user select one"""
    print("[INIT] Fetching available databases...")
    try:
        databases = database.list_databases()
        user_databases = [db for db in databases if db not in ["master", "tempdb", "model", "msdb"]]

        if not user_databases:
            print("[WARNING] No user databases found. Using 'master'")
            return "master"

        print(f"\n[INIT] Available databases:")
        for i, db in enumerate(user_databases, 1):
            print(f"  {i}. {db}")

        while True:
            try:
                choice = input(f"\nSelect database (1-{len(user_databases)}): ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(user_databases):
                    return user_databases[idx]
                print(f"Please enter a number between 1 and {len(user_databases)}")
            except ValueError:
                print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"[WARNING] Could not fetch databases: {e}. Using 'master'")
        return "master"


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("AI Data Analyst - Natural Language to SQL")
    print("="*60 + "\n")

    try:
        # Initialize configuration and analyzer
        print("[INIT] Loading configuration...")
        config = Config.from_env()
        print("[INIT] Configuration loaded\n")

        # Let user select database
        selected_db = select_database()
        config.database = selected_db

        print(f"\n[INIT] Initializing database: {selected_db}...")
        analyzer = DataAnalyzer(config)
        print(f"[INIT] Database connected")
        print(f"[INIT] Tables found: {', '.join(analyzer.schema.keys())}\n")

        # Test with sample query
        test_query = "Show me all customers from Mumbai"
        sql, results = analyzer.analyze(test_query)
        analyzer.display_results(sql, results)

        # Interactive mode (skip in Docker)
        if os.getenv("DOCKER_ENV") != "true":
            print("\n" + "="*60)
            print("Tips:")
            print("  - Ask questions in natural language")
            print("  - Type 'db' to switch databases")
            print("  - Type 'exit' or 'quit' to stop")
            print("="*60 + "\n")

            while True:
                try:
                    user_input = input("Enter your question: ").strip()

                    if user_input.lower() in ["exit", "quit", "q"]:
                        print("\nGoodbye!\n")
                        break

                    if user_input.lower() == "db":
                        new_db = select_database()
                        if new_db != analyzer.db.db_name:
                            config.database = new_db
                            analyzer = DataAnalyzer(config)
                            print(f"\n[SUCCESS] Switched to database: {new_db}")
                            print(f"[INFO] Tables found: {', '.join(analyzer.schema.keys())}\n")
                        continue

                    if not user_input:
                        continue

                    sql, results = analyzer.analyze(user_input)
                    analyzer.display_results(sql, results)

                except KeyboardInterrupt:
                    print("\n\nInterrupted. Goodbye!\n")
                    break
                except Exception as e:
                    print(f"\n[ERROR] {e}\n")
        else:
            print("\n[INFO] Running in Docker mode. Test query completed.\n")

    except ValueError as e:
        print(f"\n[ERROR] Configuration Error:\n  {e}\n")
        sys.exit(1)
    except ConnectionError as e:
        print(f"\n[ERROR] Connection Error:\n  {e}\n")
        sys.exit(1)
    except RuntimeError as e:
        print(f"\n[ERROR] Database Error:\n  {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected Error:\n  {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
