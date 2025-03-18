"""
Runs Whisper inside a web API.
Lets other apps (frontend, mobile, other programs) request transcriptions via HTTP.
Streams real-time transcriptions to the user over the internet.
"""
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json
import re

app = FastAPI()

# Enable CORS: Allow frontend (http://127.0.0.1:8001) to access backend (http://127.0.0.1:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin (use ["http://127.0.0.1:8001"] for stricter security)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

WHISPER_BINARY = "./whisper.cpp-1.7.4/build/bin/whisper-stream"
WHISPER_MODEL = "whisper.cpp-1.7.4/models/ggml-base.en.bin"

# Store active transcriptions by timestamp (avoiding overlap issues)
transcriptions = []
transcription_buffer = {}  # Stores ongoing transcriptions

def clean_transcription(text):
    """Removes unwanted artifacts like '[2K', '[BLANK_AUDIO]', and ANSI escape sequences."""
    text = re.sub(r"\[\d+[A-Za-z]", "", text)  # Remove ANSI escape sequences
    text = re.sub(r"\[BLANK_AUDIO\]", "", text, flags=re.IGNORECASE)  # Remove blank audio markers
    text = text.replace("\x1b", "").strip()  # Remove escape characters
    return text if text else None  # Return None for empty strings

# def extract_transcription_info(text):
#     """Extracts transcription ID, timestamps, and text from Whisper output."""
#     match = re.search(r"### Transcription (\d+) START \| t0 = (\d+) ms \| t1 = (\d+) ms \[.*?\] (.*?) ### Transcription \d+ END", text)
#     if match:
#         transcription_id = int(match.group(1))
#         t0 = int(match.group(2))
#         t1 = int(match.group(3))
#         transcription_text = match.group(4)
#         return transcription_id, t0, t1, transcription_text
#     return None

def extract_transcription_info(text):
    """Extracts transcription ID, timestamps, and text from Whisper messages."""
    start_match = re.match(r"### Transcription (\d+) START \| t0 = (\d+) ms \| t1 = (\d+) ms", text)
    end_match = re.match(r"### Transcription (\d+) END", text)
    actual_text_match = re.search(r"\[\d\d:\d\d:\d\d\.\d\d\d --> \d\d:\d\d:\d\d\.\d\d\d\] (.+)", text)

    if start_match:
        trans_id = int(start_match.group(1))
        t0, t1 = int(start_match.group(2)), int(start_match.group(3))
        transcription_buffer[trans_id] = {"t0": t0, "t1": t1, "text": ""}
    
    elif actual_text_match:
        extracted_text = actual_text_match.group(1)
        if transcription_buffer:
            last_trans_id = max(transcription_buffer.keys())  # Get most recent transcription ID
            transcription_buffer[last_trans_id]["text"] += " " + extracted_text.strip()

    elif end_match:
        trans_id = int(end_match.group(1))
        if trans_id in transcription_buffer:
            final_text = transcription_buffer[trans_id]["text"].strip()
            del transcription_buffer[trans_id]  # Remove completed entry
            return final_text

    return None

# def update_transcriptions(t0, t1, text):
#     """Replaces older overlapping segments with the newest refined transcription."""
#     global transcriptions

#     # Remove older transcriptions that overlap with this one
#     transcriptions = [t for t in transcriptions if not (t0 <= t["t1"] and t1 >= t["t0"])]

#     # Add new transcription
#     transcriptions.append({"t0": t0, "t1": t1, "text": text})

#     # Sort transcriptions by start time
#     transcriptions.sort(key=lambda x: x["t0"])

#     return " ".join(t["text"] for t in transcriptions)  # Return combined transcript


def stream_transcriptions():
    """Runs whisper-stream and streams cleaned live transcriptions."""
    process = subprocess.Popen(
        [WHISPER_BINARY, "-m", WHISPER_MODEL, "-t", "8", "--step", "0", "--length", "10000", "-vth", "0.6"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    last_sent_text = ""
    try:
        for line in iter(process.stdout.readline, ""):
            # cleaned_text = clean_transcription(line)
            # if cleaned_text:  # Only send non-empty transcriptions
            final_text = extract_transcription_info(line)
            if final_text:
                    message = json.dumps({"text": final_text})
                    yield f"data: {message}\n\n"
            # transcription_info = extract_transcription_info(line)
            # if transcription_info:
            #     _, t0, t1, transcription_text = transcription_info
            #     updated_transcript = update_transcriptions(t0, t1, transcription_text)
            #     message = json.dumps({"text": updated_transcript, "replace": True})
            #     yield f"data: {message}\n\n"
    finally:
        process.terminate()

@app.get("/transcribe")
def transcribe():
    """API endpoint to stream live transcriptions."""
    return StreamingResponse(stream_transcriptions(), media_type="text/event-stream")

