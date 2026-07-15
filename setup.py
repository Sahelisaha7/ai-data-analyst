"""Automated setup script for AI Data Analyst"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and report status"""
    print(f"\n{description}...")
    try:
        subprocess.check_call(cmd, shell=True)
        print(f"✓ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        return False

def check_file_exists(filename):
    """Check if a file exists"""
    return Path(filename).exists()

def main():
    """Main setup process"""
    print("\n" + "="*60)
    print("AI DATA ANALYST - SETUP WIZARD")
    print("="*60)

    # Step 1: Install dependencies
    print("\n[STEP 1] Installing Python dependencies...")
    run_command(
        "pip install openai python-dotenv sqlalchemy",
        "Installing dependencies"
    )

    # Step 2: Check .env file
    print("\n[STEP 2] Checking configuration...")
    if not check_file_exists(".env"):
        print("✗ .env file not found!")
        sys.exit(1)

    with open(".env", "r") as f:
        content = f.read()
        if "your-api-key-here" in content:
            print("⚠ WARNING: .env still has placeholder API key!")
            print("Please update .env with your OpenAI API key:")
            print("  OPENAI_API_KEY=sk-proj-your-actual-key")
            sys.exit(1)
    print("✓ Configuration found")

    # Step 3: Generate data
    print("\n[STEP 3] Generating sample data...")
    if not check_file_exists("customers.csv"):
        run_command("python generate_data.py", "Generating CSV data")
    else:
        print("✓ CSV files already exist")

    # Step 4: Load database
    print("\n[STEP 4] Loading data into database...")
    if not check_file_exists("amazon.db"):
        run_command("python load_data.py", "Loading database")
    else:
        print("✓ Database already exists")

    # Step 5: Verify setup
    print("\n[STEP 5] Verifying setup...")
    required_files = ["customers.csv", "products.csv", "orders.csv", "order_items.csv", "amazon.db", ".env"]
    all_exist = all(check_file_exists(f) for f in required_files)

    if all_exist:
        print("✓ All files verified")
    else:
        missing = [f for f in required_files if not check_file_exists(f)]
        print(f"✗ Missing files: {', '.join(missing)}")
        sys.exit(1)

    # Success!
    print("\n" + "="*60)
    print("SETUP COMPLETE! ✓")
    print("="*60)
    print("\nYou can now run the application:")
    print("  python main.py")
    print("\nThe application will:")
    print("  1. Load your database (10k+ records)")
    print("  2. Show a test query")
    print("  3. Enter interactive mode for your questions")
    print("\nExample questions:")
    print('  "Show me all customers from Mumbai"')
    print('  "What is the total revenue by city?"')
    print('  "List top 10 best-selling products"')
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
