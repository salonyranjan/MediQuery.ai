FROM python:3.10-slim-buster

WORKDIR /app

# Prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1

# Install system build tools (required for many AI / LangChain deps)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    linux-headers-amd64 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Upgrade pip and install (separated for cleaner logs)
RUN pip install --no-cache-dir --upgrade pip==26.0.1 setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Match the port in your GitHub YAML
EXPOSE 8080

CMD ["python3", "app.py"]