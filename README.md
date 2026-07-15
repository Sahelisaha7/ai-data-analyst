# 📊 AI Data Analyst

An AI-powered data analyst that converts natural language questions into SQL queries and visualizes results using Streamlit.

## Features

✨ **Natural Language to SQL**: Ask questions in plain English, get SQL queries
🤖 **AI-Powered**: Uses Deepseek model via Ollama for intelligent query generation
📊 **Beautiful UI**: Interactive Streamlit frontend with results visualization
💾 **Database Support**: SQLite with full schema inspection
📥 **Export Results**: Download query results as CSV

## Project Structure

```
ai-data-analyst/
├── main.py                 # Core logic: schema extraction, text-to-SQL, query execution
├── streamlit_app.py        # Streamlit web frontend
├── create_database.py      # Database initialization with dummy data
├── amazon.db              # SQLite database
├── pyproject.toml         # Project dependencies
└── README.md              # This file
```

## Database Schema

### Tables:
- **customers**: Customer information (name, email, city, join_date)
- **products**: Product catalog (name, category, price)
- **orders**: Customer orders (customer_id, order_date, total_amount)
- **order_items**: Order line items (order_id, product_id, quantity, subtotal)

## Setup

### Prerequisites
- Python 3.8+
- Ollama with Deepseek model installed
- UV package manager

### Installation

1. **Navigate to project directory**
```bash
cd d:\AI_data_analyst
```

2. **Install dependencies**
```bash
uv pip install sqlalchemy streamlit pandas ollama
```

3. **Ensure Ollama is running with Deepseek model**
```bash
ollama pull deepseek-r1:8b
ollama serve
```

4. **Database is already created** with sample data

## Usage

### Option 1: Run Streamlit Web App (Recommended)
```bash
streamlit run streamlit_app.py
```
Then open your browser at `http://localhost:8501`

### Option 2: Use main.py directly
```bash
python main.py
```

## Example Queries

Try asking questions like:
- "Show me all customers from Mumbai"
- "What is the total sales by category?"
- "List all orders with product details"
- "Which customers spent the most?"
- "Show me products under 2000 rupees"
- "Get all electronics in the store"

## How It Works

1. **User Input**: You ask a question in natural language
2. **Schema Extraction**: The system extracts database schema
3. **AI Conversion**: Deepseek model converts your question to SQL
4. **Query Execution**: SQL is executed on the database
5. **Results Display**: Results are shown in a beautiful table with export options

## Architecture

```
User Question
    ↓
Text-to-SQL (Ollama + Deepseek)
    ↓
SQL Query Validation
    ↓
Execute on SQLite Database
    ↓
Format Results (DataFrame)
    ↓
Display in Streamlit UI
    ↓
Option to Export (CSV)
```

## Troubleshooting

### Ollama not found
- Make sure Ollama is installed and running: `ollama serve`
- Pull the Deepseek model: `ollama pull deepseek-r1:8b`

### Port 8501 already in use
- Run on different port: `streamlit run streamlit_app.py --server.port 8502`

## Configuration

### Change Model
Edit `main.py` line 42:
```python
response = ollama.generate(
    model="deepseek-r1:8b",  # Change this
    ...
)
```

### Change Database
Edit `main.py` line 6:
```python
db_url = "sqlite:///your_database.db"
```

## Dependencies

- **sqlalchemy**: Database ORM and schema inspection
- **streamlit**: Web UI framework
- **pandas**: Data manipulation and analysis
- **ollama**: Local LLM integration

---

**Made with ❤️ for data analysis**