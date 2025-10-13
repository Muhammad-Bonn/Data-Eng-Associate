"""
extract_metadata.py
-------------------
Fetches metadata (views, likes, duration, comments) for YouTube videos
based on a list of VideoIDs.
"""
from googleapiclient.discovery import build
import pandas as pd
import isodate
import time

def extract_metadata(api_key, data):
    """
    Fetch YouTube metadata for videos listed in the given DataFrame.

    Parameters:
        api_key (str): YouTube API key
        data (pd.DataFrame): DataFrame containing a 'VideoID' column
    """
    youtube = build('youtube', 'v3', developerKey=api_key)

    if 'VideoID' not in data.columns:
        raise ValueError("DataFrame must contain a 'VideoID' column")

    video_ids = data['VideoID'].dropna().drop_duplicates().tolist()
    metadata = []

    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        try:
            request = youtube.videos().list(
                part='statistics,contentDetails',
                id=",".join(batch)
            )
            response = request.execute()
        except Exception as e:
            print(f"Error fetching batch {i//50 + 1}: {e}")
            time.sleep(2)
            continue

        for item in response.get('items', []):
            stats = item.get('statistics', {})
            details = item.get('contentDetails', {})
            duration = details.get('duration')

            metadata.append({
                'VideoID': item['id'],
                'Views': int(stats.get('viewCount', 0)),
                'Likes': int(stats.get('likeCount', 0)),
                'Comments': int(stats.get('commentCount', 0)),
                'Duration_seconds': int(isodate.parse_duration(duration).total_seconds() if duration else 0)
            })

        time.sleep(0.5)

    meta_df = pd.DataFrame(metadata)
    merged = pd.merge(data, meta_df, on='VideoID', how='left')

    print(f"Metadata fetched for {len(meta_df)} videos.")
    return merged
