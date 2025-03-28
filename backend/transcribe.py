# backend/transcribe.py

import subprocess
import json
import re
import time
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from llm import send_to_llm  # assumes this function exists in main.py

# TODO: use previous whisper-stream method. replace div on frontend until complete msg formed

router = APIRouter()

WHISPER_BINARY = "../whisper.cpp-1.7.4/build/bin/whisper-stream"
WHISPER_MODEL = "../whisper.cpp-1.7.4/models/ggml-base.en.bin"
# WHISPER_ARGS = [WHISPER_BINARY, "-m", WHISPER_MODEL, "--step", "500", "--length", "5000"]
WHISPER_ARGS = [WHISPER_BINARY, "-m", WHISPER_MODEL, "-t", "8", "--step", "0", "--length", "130000", "-vth", "1.6"]


def clean(text: str) -> str:
    """Removes unwanted artifacts like '[2K', '[BLANK_AUDIO]', noises in (), [], or *...*, and ANSI escape sequences."""
    if not text:
        return text
    text = re.sub(r"\[\d+[A-Za-z]", "", text)  # Remove ANSI escape sequences
    text = re.sub(r"\[BLANK_AUDIO\]", "", text, flags=re.IGNORECASE)  # Remove blank audio markers
    text = re.sub(r"(\(.*?\)|\[.*?\]|\*.*?\*)", "", text) # Remove non-verbal sounds in (), [], or *...*
    text = text.replace("\x1b", "").strip()  # Remove escape characters
    if is_log(text):
        return None
    return text if text else None  # Return None for empty strings

def is_log(text):
    return any([
        text.startswith("init:"),
        text.startswith("whisper_"),
        text.startswith("ggml_"),
        text.startswith("main:"),
        text.startswith("###"),
        "loading model" in text,
        "samples (" in text,
        "input is too short" in text,
        "[Start speaking]" in text,
    ])

def stream_transcription_and_reply():
    process = subprocess.Popen(
        WHISPER_ARGS,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    buffer = []
    last_spoken = time.time()
    last_cleaned = None
    seen_transcripts = set()
    MAX_HISTORY = 10

    try:
        for line in iter(process.stdout.readline, ""):
            # If some time threshold has passed since last input, consider user done
            if buffer and (time.time() - last_spoken > 2.5):
                print("2.5 seconds of silence")
                print(buffer)
                # full_text = " ".join(buffer).strip()
                full_text = buffer[-1]
                buffer.clear()
                last_cleaned = full_text
                seen_transcripts.add(full_text)

                if full_text:
                    reply = send_to_llm(full_text)
                    yield f"data: {json.dumps({'text': full_text, 'complete': True, 'reply': reply})}\n\n"

                last_spoken = time.time()
                continue

            cleaned = clean(line)
            if not cleaned:
                continue

             # Ignore duplicate transcription
            if cleaned == last_cleaned:
                continue
            if cleaned in seen_transcripts:
                continue

            print(cleaned)
            print(buffer)
            last_cleaned = cleaned
            buffer = [cleaned]
            last_spoken = time.time()
            yield f"data: {json.dumps({'text': cleaned, 'complete': False})}\n\n"

    finally:
        process.terminate()

@router.get("/transcribe")
def transcribe():
    return StreamingResponse(stream_transcription_and_reply(), media_type="text/event-stream")