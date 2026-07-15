# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY main.py .
COPY load_data.py .
COPY generate_data.py .
COPY customers.csv .
COPY products.csv .
COPY orders.csv .
COPY order_items.csv .

# Create database
RUN python load_data.py

# Expose port (for web interface)
EXPOSE 8501

# Run the application
CMD ["python", "main.py"]
