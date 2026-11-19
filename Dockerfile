# Official base image: Ubuntu 24.04 + Python + browsers for Playwright 1.65.1
FROM mcr.microsoft.com/playwright/python:v1.65.1-noble

# The folder inside the container where the project lives
WORKDIR /app

# Install Python packages first: Docker caches this step until requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project (minus what .dockerignore excludes)
COPY . .

# Default command: run the smoke tests (headless: a container has no screen)
CMD ["pytest", "-m", "smoke", "-v"]