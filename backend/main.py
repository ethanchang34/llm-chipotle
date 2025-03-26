# backend/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

# TODO: prime the llm with prompts to reduce output size and clarify goal (extract order)

app = FastAPI()

# Allow frontend dev on localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"

# Track ongoing conversation (in-memory for now)
conversation_history = []

class Message(BaseModel):
    message: str

@app.post("/chat")
def chat_with_bot(msg: Message):
    user_input = msg.message.strip()
    if not user_input:
        return {"reply": "I didn't catch that. Can you repeat?"}

    # Add user message to history
    conversation_history.append({"role": "user", "content": user_input})

    # Send full conversation to local LLM
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "messages": conversation_history,
        "stream": False
    })
    response_json = response.json()
    assistant_reply = response_json["message"]["content"].strip()

    # Add assistant reply to history
    conversation_history.append({"role": "assistant", "content": assistant_reply})

    return {"reply": assistant_reply}
