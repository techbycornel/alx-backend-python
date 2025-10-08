# Use the official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Django's default port
EXPOSE 8000

# Run Django app and include the '-p' flag as required
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000", "-p", "8000"]
