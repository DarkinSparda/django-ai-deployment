from pytubefix import YouTube
from django.conf import settings
import os
import assemblyai as aai
import whisper

def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title

def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
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

    return transcript.text

def get_transcription_whisper(link, model_size="tiny"):
    """
    Transcribe YouTube video audio using OpenAI's open-source Whisper model locally.

    Args:
        link: YouTube video URL
        model_size: Whisper model size (tiny, base, small, medium, large). Default is 'tiny' for speed.

    Returns:
        str: Transcribed text from the audio
    """
    audio_file = download_audio(link)

    # Load the Whisper model
    model = whisper.load_model(model_size)

    # Transcribe with speed optimizations
    result = model.transcribe(
        audio_file,
        fp16=False,  # Use FP32 for CPU compatibility (set to True if using GPU)
        language='en',  # Specify language to skip detection (faster)
        task='transcribe',  # Explicitly set task
        verbose=False  # Disable verbose output
    )

    # Clean up the audio file after transcription
    if os.path.exists(audio_file):
        os.remove(audio_file)

    return result['text']

