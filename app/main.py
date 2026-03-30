from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from app.auth.auth import USERS, create_access_token, get_current_user
from app.rag.pipeline import rag_pipeline, retrieve_docs
from app.llm.groq_client import generate_streaming_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 🏠 Health check
@app.get("/")
def home():
    return {"message": "RAG RBAC API is running"}


# 🔐 Login
@app.post("/login")
def login(username: str, password: str):
    user = USERS.get(username)

    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "username": username,
        "role": user["role"]
    })

    return {"access_token": token}


# 👤 Current user
@app.get("/me")
def get_me(user=Depends(get_current_user)):
    return {"user": user}


# 💬 Request schema (with memory)
class ChatRequest(BaseModel):
    query: str
    chat_history: Optional[List[str]] = []


# 🔥 Standard Chat (non-streaming)
@app.post("/chat")
def chat(request: ChatRequest, user=Depends(get_current_user)):
    result = rag_pipeline(
        request.query,
        user["role"],
        request.chat_history
    )
    return result


# ⚡ Streaming Chat (ChatGPT-like)
@app.post("/chat/stream")
def chat_stream(request: ChatRequest, user=Depends(get_current_user)):
    role = user["role"]

    # 🔍 Retrieve docs
    docs = retrieve_docs(request.query, role)

    context = "\n".join([d["text"] for d in docs])

    # 🧠 Generator function
    def stream():
        for chunk in generate_streaming_response(request.query, context):
            yield chunk

    return StreamingResponse(stream(), media_type="text/plain")