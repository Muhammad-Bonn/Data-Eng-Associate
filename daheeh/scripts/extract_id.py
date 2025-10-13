"""
extract_id.py
-------------
Fetches all video IDs and basic info from YouTube playlists.
"""
from googleapiclient.discovery import build
import pandas as pd

def extract_id(api_key, playlist_id):
    """
    Extract all videos from a single playlist.
    """
    youtube = build('youtube', 'v3', developerKey=api_key)
    videos = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            snippet = item['snippet']
            video_id = snippet['resourceId']['videoId']
            videos.append({
                'VideoID': video_id,
                'Title': snippet['title'],
                'Description': snippet['description'],
                'Channel': snippet['channelTitle'],
                'URL': f"https://www.youtube.com/watch?v={video_id}"
            })

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return pd.DataFrame(videos)


def extract_all_playlists(api_key, playlist_ids):
    """
    Extract videos from multiple playlists and combine into one DataFrame.
    """
    all_data = pd.DataFrame()
    for pid in playlist_ids:
        df = extract_id(api_key, pid)
        all_data = pd.concat([all_data, df], ignore_index=True)
    return all_data
