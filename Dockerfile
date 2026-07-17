# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for ODBC
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    unixodbc \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY app.py .
COPY main.py .
COPY database.py .
COPY .env .

# Expose Flask port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV PORT=5000

# Run the Flask application
CMD ["python", "app.py"]
