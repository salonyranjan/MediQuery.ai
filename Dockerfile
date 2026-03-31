# Use Bookworm (Debian 12) to ensure active, non-archived repositories
FROM python:3.10-slim-bookworm

WORKDIR /app

# Prevent Python from buffering logs (best for AWS/CloudWatch logs)
ENV PYTHONUNBUFFERED=1

# Install build tools - Bookworm repos will now resolve correctly
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip==26.0.1 setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Match the port in your GitHub Actions YAML and AWS Security Group
EXPOSE 8080

# Start the Flask app
CMD ["python3", "app.py"]