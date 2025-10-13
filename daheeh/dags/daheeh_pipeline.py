"""
daheeh_pipeline.py
-------------------
Airflow DAG to run the Daheeh YouTube ETL pipeline every Tuesday and Saturday at 9:30 PM.
Runs immediately once when triggered for the first time.
"""

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# ----------------------------------------------------
# Default arguments for all tasks
# ----------------------------------------------------
default_args = {
    'owner': 'muhammad_bonn',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# ----------------------------------------------------
# Define the DAG
# ----------------------------------------------------
with DAG(
    dag_id='daheeh_youtube_pipeline',
    default_args=default_args,
    description='Fetch and enrich YouTube Daheeh data, store it in SQLite',
    schedule_interval='30 21 * * 2,6',  # 9:30 PM every Tuesday and Saturday
    start_date=datetime.now(),
    catchup=False,
    tags=['daheeh', 'youtube', 'etl']
) as dag:

    # Path to scripts inside the Docker container
    scripts_path = '/opt/airflow/dags/scripts'

    # ----------------------------------------------------
    # Task 1: Extract video IDs from playlists
    # ----------------------------------------------------
    extract_ids = BashOperator(
        task_id='extract_video_ids',
        bash_command=f'cd {scripts_path} && python extract_id.py',
    )

    # ----------------------------------------------------
    # Task 2: Fetch metadata for each video
    # ----------------------------------------------------
    extract_metadata = BashOperator(
        task_id='extract_video_metadata',
        bash_command=f'cd {scripts_path} && python extract_metadata.py',
    )

    # ----------------------------------------------------
    # Task 3: Run the main pipeline (save to SQLite)
    # ----------------------------------------------------
    save_to_db = BashOperator(
        task_id='save_data_to_sqlite',
        bash_command=f'cd {scripts_path} && python main.py',
    )

    # ----------------------------------------------------
    # Set task order
    # ----------------------------------------------------
    extract_ids >> extract_metadata >> save_to_db
