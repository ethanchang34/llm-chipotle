"""
Runs Whisper inside a web API.
Lets other apps (frontend, mobile, other programs) request transcriptions via HTTP.
Streams real-time transcriptions to the user over the internet.
"""
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
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

# Chipotle menu items for basic NLP filtering
MENU_ITEMS = [
    "bowl", "burrito", "tacos", "quesadilla", "salad",
    "chicken", "steak", "barbacoa", "carnitas", "sofritas", "veggie",
    "white rice", "brown rice", "black beans", "pinto beans",
    "fajita veggies", "cheese", "sour cream", "guacamole", "lettuce",
    "mild salsa", "medium salsa", "hot salsa", "corn salsa",
    "extra", "double", "no"
]

def extract_order(text):
    """Extracts Chipotle menu items from transcriptions."""
    words = text.lower().split()
    order_items = [word for word in words if word in MENU_ITEMS]

    return " ".join(order_items) if order_items else None

def clean_transcription(text):
    """Removes unwanted artifacts like '[2K', '[BLANK_AUDIO]', and ANSI escape sequences."""
    text = re.sub(r"\[\d+[A-Za-z]", "", text)  # Remove ANSI escape sequences
    text = re.sub(r"\[BLANK_AUDIO\]", "", text, flags=re.IGNORECASE)  # Remove blank audio markers
    text = text.replace("\x1b", "").strip()  # Remove escape characters
    return text if text else None  # Return None for empty strings

def stream_transcriptions():
    """Runs whisper-stream and streams cleaned live transcriptions."""
    process = subprocess.Popen(
        [WHISPER_BINARY, "-m", WHISPER_MODEL, "-t", "8", "--step", "500", "--length", "5000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    try:
        for line in iter(process.stdout.readline, ""):
            cleaned_text = clean_transcription(line)
            if cleaned_text:  # Only send non-empty transcriptions
                extracted_order = extract_order(cleaned_text)
                yield f"data: {extracted_order if extracted_order else cleaned_text}\n\n"
    finally:
        process.terminate()

@app.get("/transcribe")
def transcribe():
    """API endpoint to stream live transcriptions."""
    return StreamingResponse(stream_transcriptions(), media_type="text/event-stream")

