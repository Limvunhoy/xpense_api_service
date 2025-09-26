# Use official Python image
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code
COPY . .

# Expose the port Cloud Run provides
ENV PORT 8080

# Run Gunicorn with Uvicorn worker
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

