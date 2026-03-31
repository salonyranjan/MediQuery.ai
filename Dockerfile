FROM python:3.10-slim-bullseye

WORKDIR /app

# Prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1

# Install only the essentials for LangChain/AI deps
RUN apt-get update --fix-missing && \
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

# Use python3 to match the slim image naming
CMD ["python3", "app.py"]