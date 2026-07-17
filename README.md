# AI Data Analyst

Convert natural language questions into SQL queries using Claude AI. Query your SQL Server database through a beautiful web interface.

## Prerequisites

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **SQL Server** - Local or cloud instance
- **Anthropic API Key** - [Get free credits](https://console.anthropic.com/)
- **Git** - For version control

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/YOUR-USERNAME/AI-data-analyst.git
cd AI-data-analyst
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create `.env` file in project root:
```
ANTHROPIC_API_KEY=your-api-key-here
SQL_DATABASE=master
```

### 5. Update SQL Server Connection
Edit `database.py` and update SQL Server credentials:
```python
SQL_SERVER_CONFIG = {
    "DRIVER": "ODBC Driver 18 for SQL Server",
    "SERVER": "YOUR-SERVER\\SQLEXPRESS",
    "DATABASE": "master",
    "Trusted_Connection": "yes",
    "TrustServerCertificate": "yes",
}
```

## Usage

### Run Locally
```bash
python app.py
```

Open browser: **http://localhost:5000**

### Features
1. **Select Database** - Choose which SQL Server database to query
2. **Ask Questions** - Write natural language questions
3. **View Results** - See generated SQL and query results in real-time

## Project Structure
```
.
├── app.py                 # Flask web application
├── main.py               # SQL generation and analysis logic
├── database.py           # SQL Server connection
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker container configuration
└── docker-compose.yml    # Docker compose setup
```

## Deployment to AWS

### Option 1: AWS App Runner (Recommended)
1. Push code to GitHub
2. Go to [AWS App Runner Console](https://console.aws.amazon.com/apprunner)
3. Create Service → Source code repository
4. Connect GitHub and select this repository
5. Configure:
   - **Runtime:** Python 3.11
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `python app.py`
6. Set Environment Variables:
   - `ANTHROPIC_API_KEY` = your API key
   - `SQL_DATABASE` = master
7. Deploy and get public URL

### Option 2: Docker
```bash
# Build image
docker build -t ai-data-analyst .

# Run container
docker run -p 5000:5000 \
  -e ANTHROPIC_API_KEY=your-api-key \
  -e SQL_DATABASE=master \
  ai-data-analyst
```

## Requirements
- Python 3.11+
- anthropic>=0.25.0
- python-dotenv>=1.0.0
- pyodbc>=5.0.0
- flask>=3.0.0

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
```bash
pip install -r requirements.txt
```

### "SQL Server connection failed"
- Verify SQL Server is running
- Check connection string in `database.py`
- Ensure ODBC driver is installed

### "Port 5000 already in use"
```bash
# Use different port
PORT=8000 python app.py
```

## License
MIT

## Support
For issues, open a GitHub issue or check the documentation.
