# 1. Use the modern stable base image (Fixes the 404 Buster error)
FROM python:3.10-slim-bookworm

WORKDIR /app

# 2. Prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1

# 3. Install ONLY what is necessary (Simplified to avoid Exit Code 100)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4. Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip==26.0.1 setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your application code
COPY . .

# 6. Expose the port used in your AWS/GitHub YAML
EXPOSE 8080

CMD ["python3", "app.py"]
