#!/bin/bash
set -e

# Step 1: Initialize Airflow metadata database (only if not initialized)
airflow db init

# Step 2: Create default user if not exists
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password 1234 || true

# Step 3: Print info
echo "Starting Airflow webserver and scheduler..."

# Step 4: Run both webserver and scheduler in background
airflow scheduler &
exec airflow webserver

