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
airflow webserver &

# Step 5: Wait for Airflow to be ready
sleep 10

# Step 6: Trigger the DAG automatically if API key is provided
if [ -n "$YOUTUBE_API_KEY" ]; then
    echo "Detected YOUTUBE_API_KEY. Triggering DAG: daheeh_youtube_pipeline ..."
    airflow dags trigger daheeh_youtube_pipeline || true
else
    echo "No YOUTUBE_API_KEY found. DAG not triggered automatically."
fi

# Keep container running
tail -f /dev/null
