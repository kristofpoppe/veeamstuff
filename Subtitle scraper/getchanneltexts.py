import requests
from youtube_transcript_api import YouTubeTranscriptApi
import re
import googleapiclient.discovery
import os
# Set your API key
api_key = 'AIzaSyB0hYNkdQZ6EFupF8a6eePWulCxrfCo1AM'

# Playlist ID from the YouTube URL you provided
playlist_id = 'PL0afnnnx_OVCdhlQvHDtQXtk-HGkX02zZ'
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

# Function to retrieve all video IDs from a playlist
def get_video_ids(playlist_id):
    video_ids = []
    next_page_token = None

    while True:
        # Construct the request URL
        url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId={playlist_id}&key={api_key}'
        if next_page_token:
            url += f'&pageToken={next_page_token}'

        # Send the GET request to the YouTube Data API
        response = requests.get(url)
        data = response.json()

        # Extract video IDs from the response
        for item in data['items']:
            video_ids.append(item['contentDetails']['videoId'])

        # Check if there are more pages
        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break

    return video_ids
def get_video_title(video_id):
    # Request the video resource
    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    # Extract the title from the response
    video_title = video_response['items'][0]['snippet']['title']

    return video_title

# Call the function to get the video IDs
video_ids = get_video_ids(playlist_id)

# Print the video IDs
for video_id in video_ids:
    try:
        srt = YouTubeTranscriptApi.get_transcript(video_id,languages=['en'])
    except:
        print(f"{video_id} doesn't have a transcript") # Skip videos with no transcripts available
    title = get_video_title(video_id)
        
    pattern = r"'text': '(.*?)', 'start'"

    with open(title+".txt", "w") as f:   
   
        # iterating through each element of list srt
        for i in srt:
            # writing each element of srt on a new line
            match = re.findall(pattern, str(i))

            if match:
                extracted_text = match[0]
                words_to_remove = ['yeah', 'uh', 'um','[Music]']
                modified_text = extracted_text

                for word in words_to_remove:
                    modified_text = modified_text.replace(word, '')
                f.write(modified_text+'\n')