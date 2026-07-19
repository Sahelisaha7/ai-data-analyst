from flask import Flask, request, jsonify
import json
import os
from dotenv import load_dotenv
from anthropic import Anthropic
import database
from main import DatabaseManager, SQLGenerator, DataAnalyzer, Config

load_dotenv()

app = Flask(__name__)

# Global state for current session
current_session = {
    "analyzer": None,
    "database": None,
    "available_databases": []
}


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


@app.route("/api/databases", methods=["GET"])
def get_databases():
    """Get list of available databases"""
    try:
        databases = database.list_databases()
        user_databases = [db for db in databases if db not in ["master", "tempdb", "model", "msdb"]]
        current_session["available_databases"] = user_databases
        return jsonify({"databases": user_databases}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/select-database", methods=["POST"])
def select_database():
    """Select a database and initialize analyzer"""
    try:
        data = request.json
        db_name = data.get("database")

        if not db_name:
            return jsonify({"error": "Database name required"}), 400

        # Initialize analyzer with selected database
        config = Config(api_key=os.getenv("ANTHROPIC_API_KEY"), database=db_name)
        analyzer = DataAnalyzer(config)

        current_session["analyzer"] = analyzer
        current_session["database"] = db_name

        tables = list(analyzer.schema.keys())
        return jsonify({
            "success": True,
            "database": db_name,
            "tables": tables,
            "table_count": len(tables)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/query", methods=["POST"])
def execute_query():
    """Execute natural language query"""
    try:
        if not current_session["analyzer"]:
            return jsonify({"error": "No database selected. Please select a database first."}), 400

        data = request.json
        user_query = data.get("query")

        if not user_query or not user_query.strip():
            return jsonify({"error": "Query cannot be empty"}), 400

        analyzer = current_session["analyzer"]

        # Generate SQL and execute
        sql_query, result = analyzer.analyze(user_query)

        return jsonify({
            "success": result["success"],
            "query": user_query,
            "sql": sql_query,
            "columns": result.get("columns", []),
            "data": result.get("data", []),
            "row_count": len(result.get("data", [])),
            "error": result.get("error")
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/current-database", methods=["GET"])
def current_database():
    """Get currently selected database"""
    return jsonify({
        "database": current_session["database"],
        "tables": list(current_session["analyzer"].schema.keys()) if current_session["analyzer"] else []
    }), 200


@app.route("/", methods=["GET"])
def index():
    """Serve simple HTML interface"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>NL-to-SQL Engine</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                border-bottom: 3px solid #007bff;
                padding-bottom: 10px;
            }
            .section {
                margin: 30px 0;
                padding: 20px;
                background-color: #f9f9f9;
                border-left: 4px solid #007bff;
                border-radius: 4px;
            }
            select, input, textarea, button {
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            select, input, textarea {
                width: 100%;
                box-sizing: border-box;
            }
            button {
                background-color: #007bff;
                color: white;
                cursor: pointer;
                border: none;
                width: 100%;
                font-weight: bold;
            }
            button:hover {
                background-color: #0056b3;
            }
            .results {
                margin-top: 20px;
                padding: 15px;
                background-color: #e7f3ff;
                border-radius: 4px;
                display: none;
            }
            .results.show {
                display: block;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }
            table, th, td {
                border: 1px solid #ddd;
            }
            th, td {
                padding: 12px;
                text-align: left;
            }
            th {
                background-color: #007bff;
                color: white;
            }
            .error {
                color: #d32f2f;
                padding: 10px;
                background-color: #ffebee;
                border-radius: 4px;
                margin: 10px 0;
            }
            .success {
                color: #388e3c;
                padding: 10px;
                background-color: #e8f5e9;
                border-radius: 4px;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 NL-to-SQL Engine</h1>

            <div class="section">
                <h2>Step 1: Select Database</h2>
                <select id="databaseSelect">
                    <option value="">Loading databases...</option>
                </select>
                <button onclick="selectDatabase()">Select Database</button>
                <div id="dbMessage"></div>
            </div>

            <div class="section">
                <h2>Step 2: Ask a Question</h2>
                <textarea id="queryInput" placeholder="e.g., Show me all customers from Mumbai" rows="4"></textarea>
                <button onclick="executeQuery()">Generate SQL & Get Results</button>
            </div>

            <div class="results" id="results">
                <h3>Results</h3>
                <div>
                    <strong>Your Question:</strong>
                    <p id="userQuery"></p>
                </div>
                <div>
                    <strong>Generated SQL:</strong>
                    <pre id="sqlQuery"></pre>
                </div>
                <div>
                    <strong>Results (<span id="rowCount">0</span> rows):</strong>
                    <div id="tableResults"></div>
                </div>
                <div id="errorMessage"></div>
            </div>
        </div>

        <script>
            // Load available databases on page load
            window.onload = function() {
                loadDatabases();
            };

            async function loadDatabases() {
                try {
                    const response = await fetch('/api/databases');
                    const data = await response.json();
                    const select = document.getElementById('databaseSelect');
                    select.innerHTML = '<option value="">Select a database...</option>';
                    data.databases.forEach(db => {
                        const option = document.createElement('option');
                        option.value = db;
                        option.textContent = db;
                        select.appendChild(option);
                    });
                } catch (error) {
                    document.getElementById('dbMessage').innerHTML = '<div class="error">Error loading databases: ' + error + '</div>';
                }
            }

            async function selectDatabase() {
                const db = document.getElementById('databaseSelect').value;
                if (!db) {
                    document.getElementById('dbMessage').innerHTML = '<div class="error">Please select a database</div>';
                    return;
                }

                try {
                    const response = await fetch('/api/select-database', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({database: db})
                    });
                    const data = await response.json();
                    if (data.success) {
                        document.getElementById('dbMessage').innerHTML =
                            '<div class="success">✓ Connected to ' + db + '<br>Tables: ' + data.tables.join(', ') + '</div>';
                    } else {
                        document.getElementById('dbMessage').innerHTML = '<div class="error">Error: ' + data.error + '</div>';
                    }
                } catch (error) {
                    document.getElementById('dbMessage').innerHTML = '<div class="error">Error selecting database: ' + error + '</div>';
                }
            }

            async function executeQuery() {
                const query = document.getElementById('queryInput').value;
                if (!query.trim()) {
                    alert('Please enter a question');
                    return;
                }

                try {
                    const response = await fetch('/api/query', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({query: query})
                    });
                    const data = await response.json();

                    document.getElementById('userQuery').textContent = data.query;
                    document.getElementById('sqlQuery').textContent = data.sql;
                    document.getElementById('rowCount').textContent = data.row_count;

                    if (data.error) {
                        document.getElementById('errorMessage').innerHTML =
                            '<div class="error">Error: ' + data.error + '</div>';
                        document.getElementById('tableResults').innerHTML = '';
                    } else {
                        document.getElementById('errorMessage').innerHTML = '';
                        if (data.data.length > 0) {
                            let html = '<table><tr>';
                            data.columns.forEach(col => {
                                html += '<th>' + col + '</th>';
                            });
                            html += '</tr>';
                            data.data.forEach(row => {
                                html += '<tr>';
                                data.columns.forEach(col => {
                                    html += '<td>' + (row[col] || '') + '</td>';
                                });
                                html += '</tr>';
                            });
                            html += '</table>';
                            document.getElementById('tableResults').innerHTML = html;
                        } else {
                            document.getElementById('tableResults').innerHTML = '<p>No results found</p>';
                        }
                    }

                    document.getElementById('results').classList.add('show');
                } catch (error) {
                    document.getElementById('errorMessage').innerHTML = '<div class="error">Error: ' + error + '</div>';
                    document.getElementById('results').classList.add('show');
                }
            }
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
