# Sparkify ETL Project

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/) 
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)

## Overview
This project implements an **ETL pipeline** to process song and log data JSON files and store them into a PostgreSQL database (`sparkifydb`).  
It consists of scripts to **create the database**, **create tables**, **load data**, and **run ETL processing**.  

---

## Table of Contents
1. [Prerequisites](#prerequisites)  
2. [Project Structure](#project-structure)  
3. [Database Setup](#database-setup)  
4. [ETL Pipeline](#etl-pipeline)  
5. [Viewing Data](#viewing-data)  
6. [Export Database](#export-database)  
7. [Notes](#notes)  

---

## Prerequisites
- Python 3.9+  
- PostgreSQL 12+ installed  
- Packages: `pandas`, `psycopg2-binary`  

Install Python packages:

```bash
pip install pandas psycopg2-binary
sparkify/
├── data/
│   ├── song_data/    # Song JSON files
│   └── log_data/     # Log JSON files
├── sql_queries.py    # SQL statements for creating/dropping/inserting tables
├── 1. create_tables.py  # Script to create/drop database tables
├── 2. etl.py            # ETL script to process song/log files
├── Result CSVs/
└── README.md         # Project documentation
