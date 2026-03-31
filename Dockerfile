# Changed from slim-buster to slim-bullseye to fix the 404 Repository error
FROM python:3.10-slim-bullseye

WORKDIR /app

# Prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1

# Install only the essentials for LangChain/AI deps
# This will now work because Bullseye repositories are active
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Upgrade pip and install
RUN pip install --no-cache-dir --upgrade pip==26.0.1 setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Match the port in your GitHub YAML/AWS setup
EXPOSE 8080

CMD ["python3", "app.py"]