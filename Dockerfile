FROM python:3.10-slim-bookworm
# Cache Buster: v1.0.1 - Forcing GitHub Actions to ignore old Buster layers
WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Step 1: Install essentials (Bookworm repos are active and 100% work)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Step 2: Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip==26.0.1 setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Step 3: Copy your project files
COPY . .

# Expose port for AWS EC2
EXPOSE 8080

CMD ["python3", "app.py"]