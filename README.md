# Daheeh YouTube Data Pipeline (Airflow + Docker)

This project automates the **YouTube data extraction pipeline** for the Arabic educational show **"الدحيح (Daheeh)"** using **Apache Airflow**, **Docker**, and **Python**.
It collects data from multiple YouTube playlists, enriches it with metadata (views, likes, duration, comments), and stores it automatically in a **SQLite database** — all inside a single Docker container.

---

## Project Structure

daheeh/
│
├── dags/
│ └── daheeh_pipeline.py # Airflow DAG to orchestrate the ETL pipeline
│
├── scripts/
│ ├── extract_id.py # Fetches all YouTube video IDs from playlists
│ ├── extract_metadata.py # Fetches metadata (views, likes, duration, etc.)
│ └── main.py # Runs full pipeline and stores data in SQLite
│
├── data/ # Output folder (created automatically)
│ └── youtube_database.db # SQLite database file (generated after run)
│
├── requirements.txt # All Python dependencies
├── Dockerfile # Container setup file
├── docker-compose.yml # Defines the Airflow service and volumes
└── entrypoint.sh # Script executed when container starts


---

## How It Works

1. When the container starts, it creates a virtual environment, installs all dependencies, and sets up Airflow.
2. The user is asked to **enter their YouTube API key** once.
3. Airflow launches the DAG:
   - `extract_id.py` → Collects video IDs from Daheeh playlists.
   - `extract_metadata.py` → Fetches metadata for each video.
   - `main.py` → Saves all results to `youtube_database.db` inside `/data`.
4. The database file is copied out of the container to your local machine after completion.

---

## How to Run

### 1. Clone this repository
`git clone https://github.com/Muhammad-Bonn/doc-data-airflow.git`
`cd doc-data-airflow/daheeh`

### 2. Build and start the container
`docker-compose up --build`

### 3. Enter your YouTube API key
Enter your YouTube API key: **** 
`You can get one via https://console.cloud.google.com/apis/credentials`

### 4. Access Airflow UI (optional)
Use the default credentials if not set otherwise:
Username: admin
Password: 1234
You’ll see the DAG daheeh_youtube_pipeline — it will trigger automatically.

### 5. Check the results
sqlite3 data/youtube_database.db
`The SQLite file will be saved in your local folder (default path: ./data/youtube_database.db).`

---

## Future Improvements
Add data cleaning and transformation tasks.
Upload data to a remote database (PostgreSQL / BigQuery).
Build visual dashboards (e.g., using Streamlit or Metabase).
Add Airflow sensors to monitor API quota usage
BigQuery).
Build visual dashboards (e.g., using Streamlit or Metabase).
Add Airflow sensors to monitor API quota usage
