# AI Data Analyst Setup Guide

## Prerequisites
- Python 3.8+
- OpenAI API Key

## Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup OpenAI API Key
1. Go to [platform.openai.com](https://platform.openai.com)
2. Click your profile → API keys
3. Create a new secret key
4. Copy the key and paste it in `.env` file:
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
```

### 3. Verify Setup
```bash
python main.py
```

You should see a test query result if everything is working.

## Usage

### Run the AI Data Analyst
```bash
python main.py
```

### Run the Web Interface (Streamlit)
```bash
streamlit run streamlit_app.py
```

## How It Works
1. **Input**: Natural language query (e.g., "Show me all customers from Mumbai")
2. **Processing**: OpenAI GPT-4o-mini converts it to SQL
3. **Execution**: SQL query runs on amazon.db
4. **Output**: Results displayed

## API Costs
- Uses GPT-4o-mini (cheapest OpenAI model)
- Typical cost: $0.01-0.05 per query
- Set your usage limits in OpenAI dashboard

## Troubleshooting

### "OPENAI_API_KEY not found"
- Check `.env` file exists in project root
- Verify key is correctly formatted
- Restart terminal/IDE

### "Invalid API key"
- Verify key from platform.openai.com
- Check for extra spaces in `.env` file
- Generate a new key if needed

### Database Connection Error
- Ensure `amazon.db` exists in project root
- Check database is not corrupted
