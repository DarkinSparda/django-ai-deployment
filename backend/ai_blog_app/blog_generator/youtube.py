from pytubefix import YouTube
from django.conf import settings
import os
import assemblyai as aai
import yt_dlp
import tempfile
import random
import time

# def yt_title(link):
#     yt = YouTube(link, client='WEB',)
#     title = yt.title
#     return title

# def download_audio(link):
#     yt = YouTube(link, client='WEB')
#     lang_code = str(list(yt.captions.keys())[0].code).split(".", 1)[-1]
#     # Try to get English audio track first
#     audio_streams = yt.streams.filter(only_audio=True)

#     # Filter for English audio tracks (audio_track_language_id is None for streams without multiple tracks)
#     english_streams = [s for s in audio_streams if s.audio_track_language_id == 'en']

#     # Prefer English audio, fallback to any audio if English not available
#     if english_streams:
#         video = english_streams[0]  # Get the first (usually highest quality) English stream
#     else:
#         video = audio_streams.first()  # Fallback to any audio stream

#     out_file = video.download(output_path=settings.MEDIA_ROOT)
#     base, ext = os.path.splitext(out_file)
#     new_file = base + '.mp3'
#     os.rename(out_file, new_file)
#     return new_file, lang_code

# def get_transcription(link):
#     audio_file, lang_code = download_audio(link)
#     aai.settings.api_key = settings.ASSEMBLY_AI_API
#     config = aai.TranscriptionConfig(language_code=lang_code)
#     transcriber = aai.Transcriber(config=config)
#     transcript = transcriber.transcribe(audio_file)

#     # Clean up the audio file after transcription
#     if os.path.exists(audio_file):
#         os.remove(audio_file)

#     return transcript.text, lang_code

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
]


def download_audio(link):
    temp_dir = tempfile.mkdtemp(prefix="yt_audio_")
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
        "retries": 3,
        "sleep_interval": 1.0,
        "max_sleep_interval": 2.5,
        "concurrent_fragment_downloads": 1,
        "nocheckcertificate": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["ios", "tv_embedded", "mediaconnect"],
                "player_skip": ["web", "android"],
            }
        },
        "outtmpl": os.path.join(temp_dir, "%(id)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "http_headers": {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "en-US,en;q=0.9",
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        downloaded_path = ydl.prepare_filename(info)

    mp3_path = os.path.splitext(downloaded_path)[0] + ".mp3"
    
    # Simple language detection
    lang_code = info.get("language")
    if not lang_code:
        # Fallback to first available caption language or 'en'
        captions = info.get("automatic_captions") or info.get("subtitles") or {}
        if captions:
            lang_code = next(iter(captions.keys())).split("-")[0]
        else:
            lang_code = "en"
            
    return mp3_path, lang_code


def get_transcription(link, api_key=None):
    audio_file, lang_code = download_audio(link)
    api_key = api_key or settings.ASSEMBLY_AI_API
    if not api_key:
        raise ValueError("AssemblyAI API key is required. Pass it explicitly or set ASSEMBLYAI_API_KEY env var.")

    aai.settings.api_key = api_key
    config = aai.TranscriptionConfig(language_code=lang_code)
    transcriber = aai.Transcriber(config=config)
    start = time.time()
    result = transcriber.transcribe(audio_file)

    if os.path.exists(audio_file):
        os.remove(audio_file)

    return result.text, lang_code

def yt_title(link):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'noplaylist': True,
        "nocheckcertificate": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["ios", "tv_embedded", "mediaconnect"],
                "player_skip": ["web", "android"],
            }
        },
        "http_headers": {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "en-US,en;q=0.9",
        },
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        return info.get('title')
