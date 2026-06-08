FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1

# Set work directory
WORKDIR /app

# Install system dependencies
# sqlite3 is required for ChromaDB
RUN apt-get update && apt-get install -y \
    build-essential \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose the port
EXPOSE $PORT

# Command to run the application
CMD uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
