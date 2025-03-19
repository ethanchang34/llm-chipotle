"""
Runs Whisper inside a web API.
Lets other apps (frontend, mobile, other programs) request transcriptions via HTTP.
Streams real-time transcriptions to the user over the internet.
"""
import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
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

# Retrieve API key securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found! Set it in your environment variables.")

openai.api_key = OPENAI_API_KEY

transcription_buffer = {}  # Stores ongoing transcriptions
transcription_segments = {}  # Stores spoken text
noise_segments = []  # Stores non-verbal noises

def send_to_llm(text, model="gpt-4-turbo"):
    """Sends transcription to a large LLM (GPT-4 or Gemini) to extract structured orders."""
    prompt = f"""
    Extract the order from this conversation and format it as JSON.
    User: "{text}"
    Output format:
    {{
        "item": "<food_item>",
        "ingredients": ["ingredient1", "ingredient2", ...]
    }}
    """

    if model.startswith("gpt"):
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(response["choices"][0]["message"]["content"])


def clean_transcription(text):
    """Removes unwanted artifacts like '[2K', '[BLANK_AUDIO]', and ANSI escape sequences."""
    text = re.sub(r"\[\d+[A-Za-z]", "", text)  # Remove ANSI escape sequences
    text = re.sub(r"\[BLANK_AUDIO\]", "", text, flags=re.IGNORECASE)  # Remove blank audio markers
    text = text.replace("\x1b", "").strip()  # Remove escape characters
    return text if text else None  # Return None for empty strings

def extract_speech_and_noises(text):
    """
    Separates spoken words from noises in a line.
    Noises are detected inside (), [], or *...* and extracted separately.
    """
    # Regex pattern to find noises inside (parentheses), [brackets], or *asterisks*
    noise_pattern = r"(\(.*?\)|\*.*?\*|\[.*?\])"
    
    # Find all noises in the line
    noises = re.findall(noise_pattern, text)
    
    # Remove noises from the text to extract only the spoken words
    spoken_text = re.sub(noise_pattern, "", text).strip()
    
    return spoken_text, noises

def extract_transcription_info(text):
    """Extracts transcription ID, timestamps, and text from Whisper messages."""
    start_match = re.match(r"### Transcription (\d+) START \| t0 = (\d+) ms \| t1 = (\d+) ms", text)
    end_match = re.match(r"### Transcription (\d+) END", text)
    actual_text_match = re.search(r"\[\d\d:\d\d:\d\d\.\d\d\d --> \d\d:\d\d:\d\d\.\d\d\d\] (.+)", text)

    if start_match:
        trans_id = int(start_match.group(1))
        t0, t1 = int(start_match.group(2)), int(start_match.group(3))
        transcription_segments[trans_id] = {"t0": t0, "t1": t1, "text": ""}

    elif actual_text_match:
        extracted_text = actual_text_match.group(1).strip()

        # Separate speech and noises
        spoken_text, noises = extract_speech_and_noises(extracted_text)

        # If there are noises, send them separately
        noise_updates = [{"text": noise, "noise": True} for noise in noises]
        if noise_updates:
            noise_segments.extend(noises)

        # If there's spoken text, store it normally
        if spoken_text:
            if transcription_segments:
                last_trans_id = max(transcription_segments.keys())  # Get latest transcription ID
                transcription_segments[last_trans_id]["text"] += " " + spoken_text
            return {"text": spoken_text, "noise": False}  # Send spoken text update
        
        return noise_updates  # Return noise messages separately

    elif end_match:
        trans_id = int(end_match.group(1))
        if trans_id in transcription_segments:
            final_text = transcription_segments[trans_id]["text"].strip()
            del transcription_segments[trans_id]  # Remove completed entry
            return {"text": final_text, "noise": False}  # Send final transcript

    return None

def stream_transcriptions():
    """Runs whisper-stream and streams cleaned live transcriptions."""
    process = subprocess.Popen(
        [WHISPER_BINARY, "-m", WHISPER_MODEL, "-t", "8", "--step", "0", "--length", "130000", "-vth", "1.6"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    try:
        for line in iter(process.stdout.readline, ""):
            cleaned_text = clean_transcription(line)

            if cleaned_text:
                updates = extract_transcription_info(cleaned_text)
                if updates:
                    if isinstance(updates, list):  # If multiple noise updates
                        for update in updates:
                            message = json.dumps(update)
                            yield f"data: {message}\n\n"
                    else:
                        message = json.dumps(updates)
                        yield f"data: {message}\n\n"
    finally:
        process.terminate()

@app.get("/transcribe")
def transcribe():
    """API endpoint to stream live transcriptions."""
    return StreamingResponse(stream_transcriptions(), media_type="text/event-stream")

