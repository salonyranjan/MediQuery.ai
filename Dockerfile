# Use Bullseye (Debian 11) to avoid EOL 'Buster' repository errors (404)
FROM python:3.10-slim-bullseye

# Set the working directory inside the container
WORKDIR /app

# Prevent Python from buffering logs (essential for CloudWatch/GitHub logs)
ENV PYTHONUNBUFFERED=1

# Install essential build tools with a retry for network stability
# We use --fix-missing to handle temporary Debian mirror glitches
RUN apt-get update --fix-missing || (sleep 5 && apt-get update --fix-missing) && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Upgrade pip and install dependencies
# We use --no-cache-dir to keep the final image size small for AWS EC2
RUN pip install --no-cache-dir --upgrade pip==26.0.1 setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files (including app.py and your data folder)
COPY . .

# Expose port 8080 to match your GitHub YAML and Flask config
EXPOSE 8080

# Start the Flask application
# Using 'python3' to ensure compatibility with the slim-bullseye image
CMD ["python3", "app.py"]