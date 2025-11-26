import requests
import re
from django.conf import settings
def get_video_id(url):
    """Extracts the video ID from a YouTube URL."""
    # Patterns for: youtube.com/watch?v=ID, youtu.be/ID, youtube.com/embed/ID
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
        r'youtube\.com\/embed\/([^&\n?#]+)',
        r'youtube\.com\/v\/([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_mp3_url(video_link):
    # The YouTube video URL you want to process
    video_id = get_video_id(video_link)

    url = "https://youtube-mp36.p.rapidapi.com/dl"

    querystring = {"id": video_id}
    headers = {
        "x-rapidapi-key": settings.RAPID_API_YT_KEY,
        "x-rapidapi-host": "youtube-mp36.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    print(response.json())
    return response.json().get('link')
