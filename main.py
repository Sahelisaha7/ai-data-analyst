import sqlite3
import json
import os
import sys
import re
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from dotenv import load_dotenv
from anthropic import Anthropic
from sqlalchemy import create_engine, inspect

load_dotenv()


@dataclass
class Config:
    """Configuration management"""
    api_key: str
    db_path: str = "amazon.db"
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
        return cls(api_key=api_key)


class DatabaseManager:
    """Handle all database operations"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.engine = None
        self.inspector = None
        self._initialize()

    def _initialize(self):
        """Initialize database connection"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(
                f"Database file not found: {self.db_path}\n"
                "Please ensure amazon.db exists in the project directory."
            )
        try:
            self.engine = create_engine(f"sqlite:///{self.db_path}")
            self.inspector = inspect(self.engine)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to database: {e}")

    def get_schema(self) -> Dict[str, List[Dict[str, str]]]:
        """Extract complete database schema"""
        schema = {}
        try:
            for table in self.inspector.get_table_names():
                columns = self.inspector.get_columns(table)
                schema[table] = [
                    {"name": col["name"], "type": str(col["type"])}
                    for col in columns
                ]
            return schema
        except Exception as e:
            raise RuntimeError(f"Failed to extract schema: {e}")

    def execute_query(self, sql_query: str) -> Dict[str, Any]:
        """Execute SQL query and return results safely"""
        if not sql_query.strip():
            return {"success": False, "error": "Empty SQL query"}

        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(sql_query)
            results = cursor.fetchall()

            if results and cursor.description:
                columns = [desc[0] for desc in cursor.description]
                data = [dict(row) for row in results]
                return {"success": True, "columns": columns, "data": data}
            else:
                return {"success": True, "columns": [], "data": []}

        except sqlite3.Error as e:
            return {"success": False, "error": f"SQL Error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
        finally:
            if conn:
                conn.close()


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
        return f"""You are a SQL expert. Convert the user's natural language question into a valid SQLite SQL query.

Database Schema:
{schema_context}

User Question: {user_query}

Rules:
- Return ONLY the SQL query, nothing else
- Use proper SQL syntax
- JOIN tables when needed
- Use aliases for clarity
- Ensure the query is valid SQLite syntax
- Handle NULL values appropriately

SQL Query:"""


class DataAnalyzer:
    """Main analyzer that orchestrates the entire process"""

    def __init__(self, config: Config):
        self.config = config
        self.client = Anthropic(api_key=config.api_key)
        self.db = DatabaseManager(config.db_path)
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

        print("[INIT] Initializing database...")
        analyzer = DataAnalyzer(config)
        print(f"[INIT] Database connected")
        print(f"[INIT] Tables found: {', '.join(analyzer.schema.keys())}\n")

        # Test with sample query
        test_query = "Show me all customers from Mumbai"
        sql, results = analyzer.analyze(test_query)
        analyzer.display_results(sql, results)

        # Interactive mode
        print("\n" + "="*60)
        print("Tips:")
        print("  - Ask questions in natural language")
        print("  - Type 'exit' or 'quit' to stop")
        print("="*60 + "\n")

        while True:
            try:
                user_input = input("Enter your question: ").strip()

                if user_input.lower() in ["exit", "quit", "q"]:
                    print("\nGoodbye!\n")
                    break

                if not user_input:
                    continue

                sql, results = analyzer.analyze(user_input)
                analyzer.display_results(sql, results)

            except KeyboardInterrupt:
                print("\n\nInterrupted. Goodbye!\n")
                break
            except Exception as e:
                print(f"\n[ERROR] {e}\n")

    except ValueError as e:
        print(f"\n[ERROR] Configuration Error:\n  {e}\n")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"\n[ERROR] File Error:\n  {e}\n")
        sys.exit(1)
    except ConnectionError as e:
        print(f"\n[ERROR] Connection Error:\n  {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected Error:\n  {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
