# backend/transcribe.py

import subprocess
import json
import re
import time
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from llm import send_to_llm  # assumes this function exists in main.py

router = APIRouter()

WHISPER_BINARY = "../whisper.cpp-1.7.4/build/bin/whisper-stream"
WHISPER_MODEL = "../whisper.cpp-1.7.4/models/ggml-base.en.bin"
WHISPER_ARGS = [WHISPER_BINARY, "-m", WHISPER_MODEL, "--step", "500", "--length", "5000"]

def clean(text: str) -> str:
    """Removes unwanted artifacts like '[2K', '[BLANK_AUDIO]', noises in (), [], or *...*, and ANSI escape sequences."""
    if not text:
        return text
    text = re.sub(r"\[\d+[A-Za-z]", "", text)  # Remove ANSI escape sequences
    text = re.sub(r"\[BLANK_AUDIO\]", "", text, flags=re.IGNORECASE)  # Remove blank audio markers
    text = re.sub(r"(\(.*?\)|\[.*?\]|\*.*?\*)", "", text) # Remove non-verbal sounds in (), [], or *...*
    text = text.replace("\x1b", "").strip()  # Remove escape characters
    return text if text else None  # Return None for empty strings

def is_log(text):
    return any([
        text.startswith("init:"),
        text.startswith("whisper_"),
        text.startswith("ggml_"),
        text.startswith("main:"),
        "loading model" in text,
        "samples (" in text,
        "input is too short" in text,
        "[Start speaking]" in text,
    ])

# def extract_speech_and_noises(text):
#     """
#     Separates spoken words from noises in a line.
#     Noises are detected inside (), [], or *...* and extracted separately.
#     """
#     # Regex pattern to find noises inside (parentheses), [brackets], or *asterisks*
#     noise_pattern = r"(\(.*?\)|\*.*?\*|\[.*?\])"
#     # Find all noises in the line
#     noises = re.findall(noise_pattern, text)
#     # Remove noises from the text to extract only the spoken words
#     spoken_text = re.sub(noise_pattern, "", text).strip()
    
#     return spoken_text, noises

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

    try:
        for line in iter(process.stdout.readline, ""):
            # If 1.5s has passed since last input, consider user done
            if buffer and (time.time() - last_spoken > 1.5):
                print("1.5 seconds of silence")
                full_text = " ".join(buffer).strip()
                buffer.clear()

                if full_text:
                    reply = send_to_llm(full_text)
                    yield f"data: {json.dumps({'reply': reply})}\n\n"

                last_spoken = time.time()
                
            cleaned = clean(line)
            if not cleaned or is_log(cleaned):
                continue
            if cleaned:
                buffer.append(cleaned)
                last_spoken = time.time()
                yield f"data: {json.dumps({'text': cleaned})}\n\n"

    finally:
        process.terminate()

@router.get("/transcribe")
def transcribe():
    return StreamingResponse(stream_transcription_and_reply(), media_type="text/event-stream")