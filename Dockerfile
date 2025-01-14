# Use a lightweight Python base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /usr/src/app

# Environment variables to optimize Python performance
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Update system packages and install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy only requirements file first for dependency caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

ENV FLASK_APP=app

# Expose the application port (ensure it matches your Flask app configuration)
EXPOSE 5000

# Set the default command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
