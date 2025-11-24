from pytubefix import YouTube
from django.conf import settings
import os
import assemblyai as aai

def yt_title(link):
    yt = YouTube(link, client='WEB',)
    title = yt.title
    return title

def download_audio(link):
    yt = YouTube(link, client='WEB')

    # Try to get English audio track first
    audio_streams = yt.streams.filter(only_audio=True)

    # Filter for English audio tracks (audio_track_language_id is None for streams without multiple tracks)
    english_streams = [s for s in audio_streams if s.audio_track_language_id == 'en']

    # Prefer English audio, fallback to any audio if English not available
    if english_streams:
        video = english_streams[0]  # Get the first (usually highest quality) English stream
    else:
        video = audio_streams.first()  # Fallback to any audio stream

    out_file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file

def get_transcription(link):
    audio_file = download_audio(link)
    aai.settings.api_key = settings.ASSEMBLY_AI_API

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)

    # Clean up the audio file after transcription
    if os.path.exists(audio_file):
        os.remove(audio_file)

    return transcript.text
