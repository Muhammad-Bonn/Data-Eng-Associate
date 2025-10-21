# Sparkify ETL Project

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/) 
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)

## Overview
This project implements an **ETL (Extract, Transform, Load) pipeline** for a music streaming service called Sparkify.  
It processes raw JSON data files containing **song information** and **user activity logs** and stores them in a structured PostgreSQL database (`sparkifydb`).  

The project demonstrates:
- Handling JSON files in Python using `pandas`.
- Populating relational database tables with foreign key relationships.
- Processing large datasets efficiently.
- Maintaining data integrity while handling missing or invalid values.

---

## Project Structure

```bash
pip install pandas psycopg2-binary
sparkify/
├── data/
│   ├── song_data/    # Song JSON files
│   └── log_data/     # Log JSON files
├── sql_queries.py    # SQL statements for creating/dropping/inserting tables
├── 1. create_tables.py  # Script to create/drop database tables
├── 2. etl.py            # ETL script to process song/log files
├── 3. ERD           # Entity-Relationship Diagram
├── Result CSVs/      # Folder for final output CSVs
└── README.md         # Project documentation
```


### Files Explanation

- **`sql_queries.py`**:  
  Contains all SQL queries for:
  - Dropping tables if they exist.
  - Creating tables (`songs`, `artists`, `users`, `time`, `songplays`).
  - Inserting records into tables.

- **`create_tables.py`**:  
  Responsible for:
  - Creating the `sparkifydb` database.
  - Dropping old tables if they exist.
  - Creating new tables with the correct schema.

- **`etl.py`**:  
  Performs the ETL pipeline:
  - Reads song JSON files → populates `songs` and `artists`.
  - Reads log JSON files → populates `users`, `time`, and `songplays`.
  - Handles missing values, skips empty or invalid records.
  - Ensures referential integrity between tables.

- **`data/song_data/`**:  
  Contains raw song JSON files, each file representing a single song and artist.

- **`data/log_data/`**:  
  Contains raw log JSON files capturing user activity, including song plays.

- **`Result CSVs/`**:  
  Optional folder for storing intermediate or final CSV outputs if needed.

