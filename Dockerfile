# Use Bullseye - it's newer and more stable than Buster
FROM python:3.10-slim-bullseye

# Set the working directory
WORKDIR /app

# Prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1

# --- STEP 1: SKIP APT-GET ENTIRELY ---
# We are removing the 'RUN apt-get' block because 99% of 
# LangChain/Groq deps don't need a C compiler anymore.

# --- STEP 2: INSTALL DEPENDENCIES ---
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# --- STEP 3: COPY CODE ---
COPY . .

# Match your AWS/GitHub port
EXPOSE 8080

# Start the bot
CMD ["python3", "app.py"]