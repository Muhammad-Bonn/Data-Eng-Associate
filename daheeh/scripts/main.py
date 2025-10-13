"""
main.py
-------
Main pipeline script for extracting and enriching YouTube video data,
then storing results in a SQLite database instead of CSV files.
"""
import sqlite3  # for database operations
from extract_id import extract_all_playlists
from extract_metadata import extract_metadata
import os

if __name__ == "__main__":
    # Your YouTube API key -- export YOUTUBE_API_KEY="*****"
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        api_key = input("Enter your YouTube API key: ").strip()    
    
    # Playlists to scrape
    playlist_ids = [
        "PL4_bo90i-4GItp18iodTK2cv-Mzn0k1es",
        "PLRCzrSHS5u_HQuXr15gOMCIK-E-57A5vd",
        "PL0ePmFx_GS-I6LJcY13e1UNdD1TJgaJvU",
        "PLAhq2Pnx-VYK6Ou-M6Fm2I3FJ2j_b3Oww",
        "PLAhq2Pnx-VYIZPcA-m7OieTUWcQ01vVPY",
        "PLAhq2Pnx-VYKbgFAxRxaNVG2p0IOsukgX",
        "PLAhq2Pnx-VYIFyJQnvl3gTEqlvRnWwnfE",
        "PLAhq2Pnx-VYIr4CjRor62E2UJMlGILErF",
        "PLAhq2Pnx-VYIZCgft9hSAHf_OuoEfsb3H",
        "PLAhq2Pnx-VYIdb7Z-Uw0IZTRCZMS3Ytrr",
        "PLAhq2Pnx-VYJSf0odwGierUaLSIaNvUUD",
        "PLAhq2Pnx-VYIMlJKtcSrYO3TXKu8KvYxv",
        "PLAhq2Pnx-VYLeu7yjrNn4KKWz8H15zFRd"
    ]

    print("Step 1: Extracting Video IDs ...")
    raw_data = extract_all_playlists(api_key, playlist_ids)
    print(f"Extracted {len(raw_data)} videos from all playlists.")

    print("\nStep 2: Extracting Metadata ...")
    enriched_data = extract_metadata(api_key, raw_data)
    print(f"Extracted metadata for {len(enriched_data)} videos.")

    print("\nStep 3: Saving data to SQLite database ...")

    # Connect to the SQLite database
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/youtube_database.db")

    # Store raw video IDs in a table
    raw_data.to_sql("raw_video_ids", conn, if_exists="replace", index=False)

    # Store enriched metadata in another table
    enriched_data.to_sql("video_metadata", conn, if_exists="replace", index=False)

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("All data saved successfully in data/youtube_database.db!")
