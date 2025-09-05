# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy requirements first (layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the code
COPY . .

# Expose port (FastAPI default 8000, Flask default 5000)
EXPOSE 5000

# Command to run your app (adjust as needed)
CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "5000"]
