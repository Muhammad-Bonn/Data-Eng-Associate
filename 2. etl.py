import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Extract data from one song JSON file and insert records into the songs and artists tables.
    """
    df = pd.read_json(filepath, lines=True)

    if df.empty:
        return  # Skip empty files

    # Handle missing or invalid year values
    year_value = int(df['year'].values[0]) if pd.notnull(df['year'].values[0]) and int(df['year'].values[0]) > 0 else None

    # Artist data first (to avoid FK issues)
    artist_lat = float(df['artist_latitude'].values[0]) if pd.notnull(df['artist_latitude'].values[0]) else None
    artist_long = float(df['artist_longitude'].values[0]) if pd.notnull(df['artist_longitude'].values[0]) else None
    artist_data = [
        df['artist_id'].values[0],
        df['artist_name'].values[0],
        df['artist_location'].values[0] if pd.notnull(df['artist_location'].values[0]) else None,
        artist_lat,
        artist_long
    ]
    cur.execute(artist_table_insert, artist_data)

    # Then insert song record
    song_data = [
        df['song_id'].values[0],
        df['title'].values[0],
        df['artist_id'].values[0],
        year_value,
        float(df['duration'].values[0])
    ]
    cur.execute(song_table_insert, song_data)


def process_log_file(cur, filepath):
    """
    Extract data from log files and insert records into the time, users, and songplays tables.
    """
    df = pd.read_json(filepath, lines=True)
    df = df[df['page'] == 'NextSong']
    if df.empty:
        return

    # Convert timestamp to datetime
    t = pd.to_datetime(df['ts'], unit='ms')

    # Insert time data
    time_df = pd.DataFrame({
        'start_time': t,
        'hour': t.dt.hour,
        'day': t.dt.day,
        'week': t.dt.isocalendar().week,
        'month': t.dt.month,
        'year': t.dt.year,
        'weekday': t.dt.day_name()
    })
    for _, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # Insert user data
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    user_df = user_df[user_df['userId'].astype(str).str.strip() != '']
    user_df.drop_duplicates(subset=['userId'], inplace=True)
    for _, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # Insert songplay records
    for _, row in df.iterrows():
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        song_id, artist_id = results if results else (None, None)

        if str(row.userId).strip() == '':
            continue

        songplay_data = (
            pd.to_datetime(row.ts, unit='ms'),
            int(row.userId),
            row.level,
            song_id,
            artist_id,
            row.sessionId,
            row.location,
            row.userAgent
        )
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Walk through all JSON files in the given directory and apply the given function.
    """
    all_files = []
    for root, dirs, files in os.walk(filepath):
        for f in glob.glob(os.path.join(root, '*.json')):
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print(f'{num_files} files found in {filepath}')

    for i, datafile in enumerate(all_files, 1):
        try:
            func(cur, datafile)
            conn.commit()
        except Exception as e:
            # Short message only, no full traceback
            print(f"[{i}/{num_files}] Skipped file due to error: {os.path.basename(datafile)}")
            conn.rollback()
        if i % 100 == 0 or i == num_files:
            print(f"→ {i}/{num_files} files processed.")


def main():
    """
    Main ETL entry point.
    """
    try:
        conn = psycopg2.connect("host=localhost dbname=sparkifydb user=postgres password=1234")
        cur = conn.cursor()

        print("Processing song_data ...")
        process_data(cur, conn, filepath='data/song_data', func=process_song_file)

        print("\nProcessing log_data ...")
        process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    except Exception as e:
        print(f"Database connection or ETL error: {e}")
    finally:
        conn.close()
        print("\nETL process completed.")


if __name__ == "__main__":
    main()
