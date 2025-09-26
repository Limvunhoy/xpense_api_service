# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Cloud Run expects your service to bind to $PORT
ENV PORT=8080

# Run FastAPI with Uvicorn
CMD exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
