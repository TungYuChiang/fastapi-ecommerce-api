FROM --platform=linux/arm64 python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install markdownlint for markdown linting
RUN npm install -g markdownlint-cli

# Copy dependency file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install ruff for Python linting
RUN pip install --no-cache-dir ruff

# Create test report directory
RUN mkdir -p /app/test-reports

# Copy application code
COPY . .

# Expose FastAPI application port
EXPOSE 8000

# Default startup command (can be overridden by docker-compose.yml)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 