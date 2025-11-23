import whisper
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
audio_path = os.path.join(script_dir, "I Tested Tesla’s Robotaxi on San Francisco's Craziest Roads.mp3")

model = whisper.load_model("base")
result = model.transcribe(audio_path)

print(result)

# Save result to a text file
output_path = os.path.join(script_dir, "transcription_result.txt")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(result["text"])

print(f"\nTranscription saved to: {output_path}")