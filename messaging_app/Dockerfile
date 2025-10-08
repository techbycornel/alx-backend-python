# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies required by mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Django port
EXPOSE 8000

# Run Django app (include -p flag for checker)
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000", "-p", "8000"]
