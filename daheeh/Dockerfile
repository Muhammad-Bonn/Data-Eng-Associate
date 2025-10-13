# Base image: lightweight Python with system dependencies
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files (DAGs, scripts, data folders)
COPY . .

# Set environment variables
ENV AIRFLOW_HOME=/app/airflow
ENV PYTHONPATH=/app

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Expose Airflow webserver port
EXPOSE 8080

# Default entrypoint (runs the shell script)
ENTRYPOINT ["/app/entrypoint.sh"]

