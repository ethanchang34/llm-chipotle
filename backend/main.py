# backend/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transcribe import router as transcribe_router
from llm import send_to_llm

app = FastAPI()

# Allow frontend dev on localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the /transcribe route
app.include_router(transcribe_router)

class Message(BaseModel):
    message: str

@app.post("/chat")
def chat_with_bot(msg: Message):
    return {"reply": send_to_llm(msg.message)}
