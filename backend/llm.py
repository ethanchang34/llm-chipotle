# backend/llm.py

import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "mistral"

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a fast, friendly Chipotle ordering assistant. "
        "Only help users place an order from the Chipotle menu. "
        "Keep replies short and structured. Never explain. "
        "Only confirm or ask clarifying questions. Keep responses under 20 words."
    )
}

conversation_history = [SYSTEM_PROMPT]

def send_to_llm(text: str) -> str:
    user_input = text.strip()
    if not user_input:
        return "I didn't catch that. Can you repeat?"

    conversation_history.append({"role": "user", "content": user_input})

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "messages": conversation_history,
        "stream": False
    })
    response_json = response.json()
    assistant_reply = response_json["message"]["content"].strip()

    conversation_history.append({"role": "assistant", "content": assistant_reply})

    return assistant_reply
