# AI Data Analyst - Industry Level Setup

A professional-grade natural language to SQL converter powered by OpenAI, with a realistic database of 10k+ records.

## Project Structure

```
AI_data_analyst/
├── main.py                 # Main application
├── generate_data.py        # Generate 10k+ sample data
├── load_data.py           # Load CSV into SQLite
├── requirements.txt        # Python dependencies
├── .env                   # API keys (create this)
├── amazon.db              # SQLite database (auto-created)
├── customers.csv          # Auto-generated
├── products.csv           # Auto-generated
├── orders.csv             # Auto-generated
└── order_items.csv        # Auto-generated
```

## Quick Start (5 minutes)

### Step 1: Install Dependencies
```bash
pip install openai python-dotenv sqlalchemy
```

### Step 2: Generate Sample Data
```bash
python generate_data.py
```
This creates:
- `customers.csv` (1,000 rows)
- `products.csv` (500 rows)
- `orders.csv` (5,000 rows)
- `order_items.csv` (~10,000 rows)

### Step 3: Load Data into Database
```bash
python load_data.py
```
This creates `amazon.db` SQLite database with 4 related tables.

### Step 4: Set Up OpenAI API Key
1. Get your API key: https://platform.openai.com/account/api-keys
2. Open `.env` file
3. Replace placeholder with your key:
```
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

### Step 5: Run the Application
```bash
python main.py
```

## Database Schema

### customers (1,000 rows)
- customer_id (Primary Key)
- first_name
- last_name
- email
- city
- phone
- join_date

### products (500 rows)
- product_id (Primary Key)
- product_name
- category
- price
- stock
- description

### orders (5,000 rows)
- order_id (Primary Key)
- customer_id (Foreign Key)
- order_date
- total_amount
- status

### order_items (~10,000 rows)
- item_id (Primary Key)
- order_id (Foreign Key)
- product_id (Foreign Key)
- quantity
- unit_price
- total_price

## Example Queries

Once running, you can ask questions like:

```
"Show me all customers from Mumbai"
"What is the total revenue by city?"
"List top 10 best-selling products"
"Show orders from last 30 days"
"Which customers spent the most?"
"Show products in Electronics category"
"Average order value by city"
```

## Features

✅ Natural language to SQL conversion using OpenAI GPT  
✅ Real database with 10k+ sample records  
✅ Production-ready error handling  
✅ Interactive query mode  
✅ Beautiful formatted results  
✅ Type hints and documentation  
✅ Secure API key management  

## Troubleshooting

### "OPENAI_API_KEY not found"
- Check `.env` file exists in project root
- Verify API key format: `OPENAI_API_KEY=sk-proj-...`
- Restart terminal after changing `.env`

### "Database file not found"
- Run `python load_data.py` first
- Ensure `amazon.db` is created

### "Module not found"
```bash
pip install openai python-dotenv sqlalchemy
```

### Results showing incorrect data
- Delete `amazon.db`
- Run `python load_data.py` again

## API Costs

- Model: GPT-4o-mini (cheapest)
- Typical cost: $0.01-0.05 per query
- Monitor usage at: https://platform.openai.com/account/usage/overview

## Files Generated

After running `generate_data.py`:
- `customers.csv` - 1,000 customer records
- `products.csv` - 500 product records
- `orders.csv` - 5,000 order records
- `order_items.csv` - ~10,000 order item records

**Total Data Points:** ~16,500 rows

## Security Notes

- ⚠️ Never commit `.env` file to git
- ⚠️ Never share your API key
- ✅ API key is automatically loaded from `.env`
- ✅ All credentials stored locally

## Next Steps

1. Customize the data generation in `generate_data.py` for your needs
2. Add more tables or relationships as needed
3. Deploy using Docker (coming soon)
4. Create a web interface with Streamlit (optional)

## Support

For issues or questions:
- Check OpenAI API status: https://status.openai.com
- API documentation: https://platform.openai.com/docs

---

**Version:** 1.0  
**Last Updated:** 2026-07-13  
**Status:** Production Ready ✓
