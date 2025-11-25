from pytubefix import YouTube
from django.conf import settings
import os
import assemblyai as aai
import yt_dlp
import tempfile
import random
import time
import re
from .mp3_api_client import get_mp3_url, get_video_id



def get_youtube_metadata(link):
    """Fetch video metadata using YouTube Data API v3 via direct HTTP request"""
    import requests

    video_id = get_video_id(link)
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    # Make direct HTTP request to YouTube Data API v3
    url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'snippet',
        'id': video_id,
        'key': settings.YOUTUBE_API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise exception for 4xx/5xx errors

    data = response.json()

    if not data.get('items'):
        raise ValueError(f"Video not found: {video_id}")

    snippet = data['items'][0]['snippet']
    title = snippet['title']
    default_audio_language = snippet.get('defaultAudioLanguage', 'en')

    # Extract just the language code (e.g., 'en' from 'en-US')
    lang_code = default_audio_language.split('-')[0]

    return title, lang_code

def yt_title(link):
    """Get YouTube video title using official API"""
    title, _ = get_youtube_metadata(link)
    return title

def download_audio(link):
    """Download audio and get language code"""
    import requests

    # Get language from YouTube API
    _, lang_code = get_youtube_metadata(link)

    # Get MP3 download URL from RapidAPI
    download_url = get_mp3_url(link)

    if not download_url:
        raise ValueError("Failed to get download URL from RapidAPI")

    # Download the MP3 file
    print(f"Downloading from: {download_url}")
    response = requests.get(download_url, stream=True)
    response.raise_for_status()

    # Extract video ID for filename
    video_id = get_video_id(link)
    output_path = os.path.join(settings.MEDIA_ROOT, f"{video_id}.mp3")

    # Save the file
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print("Downloaded using RapidAPI")
    return output_path, lang_code

def get_transcription(link):
    audio_file, lang_code = download_audio(link)
    aai.settings.api_key = settings.ASSEMBLY_AI_API
    config = aai.TranscriptionConfig(language_code=lang_code)
    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(audio_file)

    # Clean up the audio file after transcription
    if os.path.exists(audio_file):
        os.remove(audio_file)

    return transcript.text, lang_code



# PROXY_URL = "http://80y5euprwg4shi3-country-us:7QwTP5j2XrOFq6g@resi.rainproxy.io:9090"

# def download_audio(youtube_url: str, output_dir: str = "/tmp") -> str:
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'proxy': PROXY_URL,
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#         'outtmpl': f'{output_dir}/%(id)s.%(ext)s',
#         'quiet': True,
#     }
    
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(youtube_url, download=True)
#         return f"{output_dir}/{info['id']}.mp3"
    



# def get_transcription(link, api_key=None):
#     audio_file, lang_code = download_audio(link)
#     api_key = api_key or settings.ASSEMBLY_AI_API
#     if not api_key:
#         raise ValueError("AssemblyAI API key is required. Pass it explicitly or set ASSEMBLYAI_API_KEY env var.")

#     aai.settings.api_key = api_key
#     config = aai.TranscriptionConfig(language_code=lang_code)
#     transcriber = aai.Transcriber(config=config)
#     start = time.time()
#     result = transcriber.transcribe(audio_file)

#     if os.path.exists(audio_file):
#         os.remove(audio_file)

#     return result.text, lang_code

# def yt_title(link):
#     ydl_opts = {
#         'quiet': True,
#         'skip_download': True,
#         'noplaylist': True,
#         'proxy': PROXY_URL,
#         "nocheckcertificate": True,
#         "extractor_args": {
#             "youtube": {
#                 "player_client": ["ios", "tv_embedded", "mediaconnect"],
#                 "player_skip": ["web", "android"],
#             }
#         },
#         "http_headers": {
#             "User-Agent": random.choice(USER_AGENTS),
#             "Accept-Language": "en-US,en;q=0.9",
#         },
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(link, download=False)
#         return info.get('title')



# def download_audio(link):
#     temp_dir = tempfile.mkdtemp(prefix="yt_audio_")
#     ydl_opts = {
#         "format": "bestaudio/best",
#         "quiet": True,
#         "noplaylist": True,
#         "retries": 3,
#         "sleep_interval": 1.0,
#         "max_sleep_interval": 2.5,
#         "concurrent_fragment_downloads": 1,
#         "nocheckcertificate": True,
#         "extractor_args": {
#             "youtube": {
#                 "player_client": ["ios", "tv_embedded", "mediaconnect"],
#                 "player_skip": ["web", "android"],
#             }
#         },
#         "outtmpl": os.path.join(temp_dir, "%(id)s.%(ext)s"),
#         "postprocessors": [
#             {
#                 "key": "FFmpegExtractAudio",
#                 "preferredcodec": "mp3",
#                 "preferredquality": "192",
#             }
#         ],
#         "http_headers": {
#             "User-Agent": random.choice(USER_AGENTS),
#             "Accept-Language": "en-US,en;q=0.9",
#         },
#     }

    # with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #     info = ydl.extract_info(link, download=True)
    #     downloaded_path = ydl.prepare_filename(info)

    # mp3_path = os.path.splitext(downloaded_path)[0] + ".mp3"
    
    # # Simple language detection
    # lang_code = info.get("language")
    # if not lang_code:
    #     # Fallback to first available caption language or 'en'
    #     captions = info.get("automatic_captions") or info.get("subtitles") or {}
    #     if captions:
    #         lang_code = next(iter(captions.keys())).split("-")[0]
    #     else:
    #         lang_code = "en"
            
    # return mp3_path, lang_code